import React, { useEffect, useState, useRef } from 'react';
import { Upload, Info, Shield, Zap, Wifi, WifiOff, Loader2 } from 'lucide-react';
import { ConnectionStatus } from './components/ConnectionStatus';
import { FileTransferItem } from './components/FileTransferItem';
import { Button } from './components/Button';
import { generateShortId, formatBytes } from './utils/formatters';
import { MessageType, PeerMessage, FileProgress, FileMeta, CHUNK_SIZE } from './types';

// Access global PeerJS if imported via CDN
declare const Peer: any;

// Namespace to prevent collisions on public PeerJS server
const APP_PREFIX = 'AIRSHARE_P2P_V1_';

export default function App() {
  const [myId, setMyId] = useState<string>('');
  const [displayName, setDisplayName] = useState<string>('');
  const [connectedPeer, setConnectedPeer] = useState<{ id: string; name: string } | null>(null);
  const [transfers, setTransfers] = useState<FileProgress[]>([]);
  const [connectionInput, setConnectionInput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  // Refs for non-rendering state and performance
  const peerRef = useRef<any>(null);
  const connRef = useRef<any>(null);
  const incomingFilesRef = useRef<{ [key: string]: { meta: FileMeta; chunks: Blob[]; receivedSize: number; startTime: number; lastUpdate: number; bytesSinceLastUpdate: number } }>({});
  const outgoingFilesRef = useRef<{ [key: string]: { startTime: number; lastUpdate: number; bytesSent: number; bytesSinceLastUpdate: number } }>({});

  // Network status listeners
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Check for URL param to auto-fill ID
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const connectTo = params.get('connect');
    if (connectTo && connectTo.length === 4) {
      setConnectionInput(connectTo.toUpperCase());
    }
  }, []);

  // Initialize Peer
  useEffect(() => {
    const shortId = generateShortId();
    const fullId = `${APP_PREFIX}${shortId}`;
    const name = 'Device-' + Math.floor(Math.random() * 1000);
    
    setMyId(shortId); // Display only the short ID
    setDisplayName(name);

    const peer = new Peer(fullId, {
      host: '0.peerjs.com',
      port: 443,
      secure: true, // CRITICAL: Must be true for Render/HTTPS
      debug: 1,
      config: {
        iceServers: [
          { urls: 'stun:stun.l.google.com:19302' },
          { urls: 'stun:global.stun.twilio.com:3478' },
          { urls: 'stun:stun1.l.google.com:19302' },
          { urls: 'stun:stun2.l.google.com:19302' },
        ],
      },
    });

    peer.on('open', (id: string) => {
      console.log('My Peer ID is: ' + id);
      setError(null);
    });

    peer.on('connection', (conn: any) => {
      handleConnection(conn);
    });

    peer.on('error', (err: any) => {
      console.error(err);
      setIsConnecting(false);
      if (err.type === 'peer-unavailable') {
        setError(`Device ID not found. Check if the other device is online.`);
      } else if (err.type === 'network') {
        setError('Network error. Please check your Wi-Fi connection.');
      } else if (err.type === 'unavailable-id') {
         // Very rare collision retry logic
         setError('ID Collision. Retrying...');
         setTimeout(() => window.location.reload(), 1000);
      } else {
        setError('Connection error: ' + err.type);
      }
    });

    peerRef.current = peer;

    return () => {
      peer.destroy();
    };
  }, []);

  const handleConnection = (conn: any) => {
    // Close existing connection if any
    if (connRef.current && connRef.current.peer !== conn.peer) {
      connRef.current.close();
    }

    connRef.current = conn;

    conn.on('open', () => {
      // Send our display name immediately
      conn.send({
        type: MessageType.HANDSHAKE,
        payload: { name: displayName }
      });
      setError(null);
      setIsConnecting(false);
    });

    conn.on('data', (data: PeerMessage) => {
      handleData(data);
    });

    conn.on('close', () => {
      setConnectedPeer(null);
      connRef.current = null;
      setError("Peer disconnected");
      setTransfers(prev => prev.map(t => t.status === 'transferring' ? { ...t, status: 'error' } : t));
    });

    conn.on('error', (err: any) => {
      console.error('Connection error:', err);
      setError('Connection lost.');
      setIsConnecting(false);
    });
  };

  const connectToPeer = (e: React.FormEvent) => {
    e.preventDefault();
    if (!connectionInput || !peerRef.current) return;
    
    // Prevent self-connection
    if (connectionInput.toUpperCase() === myId) {
      setError("You cannot connect to yourself.");
      return;
    }

    if (!isOnline) {
      setError("Internet connection required to establish initial pairing.");
      return;
    }

    setIsConnecting(true);
    setError(null);

    const targetFullId = `${APP_PREFIX}${connectionInput.toUpperCase()}`;
    
    // Add reliable: true for better large file handling
    const conn = peerRef.current.connect(targetFullId, { reliable: true });
    
    // Connection timeout failsafe
    const timeoutTimer = setTimeout(() => {
      if (!conn.open) {
        conn.close();
        setIsConnecting(false);
        setError("Connection timed out. Devices might be behind firewalls preventing P2P.");
      }
    }, 15000); // Increased to 15s for slow networks

    // Hook into the connection events we just created
    conn.on('open', () => {
      clearTimeout(timeoutTimer);
      // handleConnection will be called inside the peer.connect logic or we call it here
      handleConnection(conn);
    });

    conn.on('error', (err: any) => {
      clearTimeout(timeoutTimer);
      setIsConnecting(false);
    });
  };

  const handleData = (message: PeerMessage) => {
    switch (message.type) {
      case MessageType.HANDSHAKE:
        setConnectedPeer({
          id: connRef.current.peer,
          name: message.payload.name
        });
        setError(null);
        break;

      case MessageType.FILE_META:
        const meta: FileMeta = message.payload;
        incomingFilesRef.current[meta.id] = {
          meta,
          chunks: [],
          receivedSize: 0,
          startTime: Date.now(),
          lastUpdate: Date.now(),
          bytesSinceLastUpdate: 0
        };
        setTransfers(prev => [...prev, {
          id: meta.id,
          fileName: meta.name,
          fileSize: meta.size,
          progress: 0,
          direction: 'incoming',
          status: 'transferring',
          speed: '0 MB/s'
        }]);
        break;

      case MessageType.FILE_CHUNK:
        const { fileId, chunk } = message.payload;
        const fileContext = incomingFilesRef.current[fileId];
        
        if (fileContext) {
          fileContext.chunks.push(new Blob([chunk]));
          fileContext.receivedSize += chunk.byteLength;
          fileContext.bytesSinceLastUpdate += chunk.byteLength;

          const now = Date.now();
          // Update UI roughly every 500ms
          if (now - fileContext.lastUpdate > 500 || fileContext.receivedSize >= fileContext.meta.size) {
            const progress = Math.min(100, (fileContext.receivedSize / fileContext.meta.size) * 100);
            
            // Calculate speed
            const timeDiff = (now - fileContext.lastUpdate) / 1000; // seconds
            const speedBytes = fileContext.bytesSinceLastUpdate / timeDiff;
            const speedStr = formatBytes(speedBytes) + '/s';

            fileContext.lastUpdate = now;
            fileContext.bytesSinceLastUpdate = 0;

            setTransfers(prev => prev.map(t => {
              if (t.id === fileId) {
                return { ...t, progress, speed: speedStr };
              }
              return t;
            }));
          }

          // Check if complete
          if (fileContext.receivedSize >= fileContext.meta.size) {
            const blob = new Blob(fileContext.chunks, { type: fileContext.meta.type });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileContext.meta.name;
            a.click();
            URL.revokeObjectURL(url);

            setTransfers(prev => prev.map(t => {
              if (t.id === fileId) {
                return { ...t, status: 'completed', progress: 100, speed: '' };
              }
              return t;
            }));
            
            delete incomingFilesRef.current[fileId];
          }
        }
        break;
    }
  };

  const sendFile = async (file: File) => {
    if (!connRef.current || !connectedPeer) return;

    const fileId = Math.random().toString(36).substring(7);
    
    // Initialize outgoing context
    outgoingFilesRef.current[fileId] = {
      startTime: Date.now(),
      lastUpdate: Date.now(),
      bytesSent: 0,
      bytesSinceLastUpdate: 0
    };

    setTransfers(prev => [{
      id: fileId,
      fileName: file.name,
      fileSize: file.size,
      progress: 0,
      direction: 'outgoing',
      status: 'transferring',
      speed: 'Starting...'
    }, ...prev]);

    connRef.current.send({
      type: MessageType.FILE_META,
      payload: {
        id: fileId,
        name: file.name,
        size: file.size,
        type: file.type
      } as FileMeta
    });

    let offset = 0;
    const reader = new FileReader();

    const sendNextChunk = () => {
      // Check if connection is still open
      if (!connRef.current || !connRef.current.open) {
        setTransfers(prev => prev.map(t => t.id === fileId ? { ...t, status: 'error' } : t));
        return;
      }

      // Backpressure check: Don't overload the data channel
      if (connRef.current.dataChannel?.bufferedAmount > 16 * 1024 * 1024) { // 16MB limit
        setTimeout(sendNextChunk, 50); // Wait a bit for buffer to clear
        return;
      }

      const slice = file.slice(offset, offset + CHUNK_SIZE);
      reader.readAsArrayBuffer(slice);
    };

    reader.onload = (e) => {
      if (e.target?.result && connRef.current) {
        const chunk = e.target.result as ArrayBuffer;
        
        try {
          connRef.current.send({
            type: MessageType.FILE_CHUNK,
            payload: {
              fileId,
              chunk,
              offset
            }
          });
        } catch (err) {
          console.error("Send error", err);
          setTransfers(prev => prev.map(t => t.id === fileId ? { ...t, status: 'error' } : t));
          return;
        }

        offset += chunk.byteLength;
        
        // Update metrics
        const ctx = outgoingFilesRef.current[fileId];
        if (ctx) {
          ctx.bytesSent = offset;
          ctx.bytesSinceLastUpdate += chunk.byteLength;
          
          const now = Date.now();
          if (now - ctx.lastUpdate > 500 || offset >= file.size) {
            const progress = (offset / file.size) * 100;
            const timeDiff = (now - ctx.lastUpdate) / 1000;
            const speedBytes = ctx.bytesSinceLastUpdate / (timeDiff || 1);
            const speedStr = formatBytes(speedBytes) + '/s';

            ctx.lastUpdate = now;
            ctx.bytesSinceLastUpdate = 0;

            setTransfers(prev => prev.map(t => {
              if (t.id === fileId) {
                return { ...t, progress, speed: speedStr };
              }
              return t;
            }));
          }
        }

        if (offset < file.size) {
          // Use 0 timeout to allow UI updates and event loop to breath, 
          // but rely on backpressure check at top of function for flow control
          setTimeout(sendNextChunk, 0); 
        } else {
           setTransfers(prev => prev.map(t => {
            if (t.id === fileId) {
              return { ...t, status: 'completed', progress: 100, speed: '' };
            }
            return t;
          }));
          delete outgoingFilesRef.current[fileId];
        }
      }
    };

    sendNextChunk();
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      Array.from(e.target.files).forEach(file => sendFile(file));
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
       Array.from(e.dataTransfer.files).forEach(file => sendFile(file));
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 p-4 md:p-8 max-w-6xl mx-auto">
      {/* Header */}
      <header className="flex flex-col md:flex-row items-center justify-between mb-8 gap-4">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Zap className="text-white" size={24} fill="currentColor" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">AirShare <span className="text-blue-400 font-light">P2P</span></h1>
        </div>
        
        <div className="flex items-center gap-4 flex-wrap justify-center">
          {/* Online/Offline Indicator */}
          <div className={`flex items-center gap-2 text-sm px-3 py-1 rounded-full border ${isOnline ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-amber-500/10 border-amber-500/30 text-amber-400'}`}>
            {isOnline ? <Wifi size={14} /> : <WifiOff size={14} />}
            <span className="hidden sm:inline">{isOnline ? 'Signal Connected' : 'Offline'}</span>
          </div>

          <div className="hidden md:flex items-center gap-2 text-sm text-slate-400 bg-slate-800/50 px-3 py-1 rounded-full border border-slate-700">
            <Shield size={14} />
            <span>End-to-End Encrypted</span>
          </div>
        </div>
      </header>

      {/* Main Connection Status */}
      <ConnectionStatus 
        myId={myId}
        displayName={displayName}
        connectedTo={connectedPeer?.id}
        connectedPeerName={connectedPeer?.name}
        onDisconnect={() => {
          if (connRef.current) connRef.current.close();
          setConnectedPeer(null);
          setTransfers([]);
          setConnectionInput('');
        }}
      />

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-200 p-4 rounded-xl mb-8 flex items-center gap-3 animate-in fade-in slide-in-from-top-2">
          <Info size={20} />
          {error}
        </div>
      )}

      {/* Main Content Area */}
      <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Connection or Drop Zone */}
        <div className="lg:col-span-1 space-y-6">
          {!connectedPeer ? (
            <div className="bg-slate-800/30 border border-slate-700 rounded-2xl p-6 relative overflow-hidden">
              {!isOnline && (
                 <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-10 p-6 text-center">
                   <div>
                     <WifiOff size={32} className="mx-auto mb-2 text-slate-500" />
                     <p className="text-slate-300 font-medium">Internet Required</p>
                     <p className="text-xs text-slate-500 mt-1">You need internet to find peers. Once connected, file sharing is offline/local.</p>
                   </div>
                 </div>
              )}
              <h2 className="text-xl font-semibold mb-4 text-white">Connect Device</h2>
              <p className="text-slate-400 text-sm mb-6">
                Enter the ID from the other device to pair securely.
              </p>
              <form onSubmit={connectToPeer} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Peer ID</label>
                  <input
                    type="text"
                    value={connectionInput}
                    onChange={(e) => setConnectionInput(e.target.value.toUpperCase())}
                    placeholder="e.g. X9Y2"
                    disabled={isConnecting}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-lg uppercase tracking-wider disabled:opacity-50"
                    maxLength={4}
                  />
                </div>
                <Button 
                  type="submit" 
                  fullWidth 
                  disabled={!connectionInput || connectionInput.length < 4 || !isOnline || isConnecting}
                  className="flex items-center justify-center gap-2"
                >
                  {isConnecting ? (
                    <>
                      <Loader2 size={18} className="animate-spin" />
                      Connecting...
                    </>
                  ) : (
                    'Connect'
                  )}
                </Button>
              </form>
              <div className="mt-6 pt-6 border-t border-slate-700/50">
                <div className="flex items-start gap-3 text-xs text-slate-500">
                  <Info size={16} className="flex-shrink-0 mt-0.5" />
                  <p>Internet is only used to find the other device. Actual file transfer happens directly over your local Wi-Fi.</p>
                </div>
              </div>
            </div>
          ) : (
            <div 
              className={`border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center transition-all cursor-pointer min-h-[300px] ${isDragOver ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 hover:border-slate-600 bg-slate-800/30'}`}
              onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
              onDragLeave={() => setIsDragOver(false)}
              onDrop={handleDrop}
              onClick={() => document.getElementById('fileInput')?.click()}
            >
              <input 
                type="file" 
                id="fileInput" 
                className="hidden" 
                multiple 
                onChange={handleFileSelect} 
              />
              <div className="h-16 w-16 bg-slate-700 rounded-full flex items-center justify-center mb-4 text-blue-400">
                <Upload size={32} />
              </div>
              <h3 className="text-lg font-medium text-white mb-2">Send Files</h3>
              <p className="text-slate-400 text-sm max-w-[200px]">
                Drag and drop files here or click to browse
              </p>
            </div>
          )}
        </div>

        {/* Right Column: Transfer History */}
        <div className="lg:col-span-2">
          <div className="bg-slate-800/30 border border-slate-700 rounded-2xl p-6 min-h-[500px] flex flex-col">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-white">Transfers</h2>
              <span className="text-sm text-slate-400">{transfers.length} files</span>
            </div>

            <div className="space-y-4 flex-1 overflow-y-auto pr-2 max-h-[600px]">
              {transfers.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center opacity-50">
                  <div className="inline-block p-4 rounded-full bg-slate-800 mb-4 text-slate-600">
                    <Upload size={24} />
                  </div>
                  <p className="text-slate-500">No active transfers</p>
                </div>
              ) : (
                [...transfers].reverse().map((transfer) => (
                  <FileTransferItem key={transfer.id} transfer={transfer} />
                ))
              )}
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}