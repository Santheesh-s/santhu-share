import React, { useEffect, useState, useRef } from 'react';
import { Upload, Info, Shield, Zap, Wifi, WifiOff, Loader2, AlertTriangle, RefreshCw } from 'lucide-react';
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
  // Initialize ID and Name lazily so they stay constant across re-renders
  const [myId] = useState(() => generateShortId());
  const [displayName] = useState(() => 'Device-' + Math.floor(Math.random() * 1000));
  
  const [connectedPeer, setConnectedPeer] = useState<{ id: string; name: string } | null>(null);
  const [transfers, setTransfers] = useState<FileProgress[]>([]);
  const [connectionInput, setConnectionInput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [isPeerReady, setIsPeerReady] = useState(false);
  const [iceState, setIceState] = useState<string>('new');

  // Refs for non-rendering state and performance
  const peerRef = useRef<any>(null);
  const connRef = useRef<any>(null);
  const connectingToRef = useRef<string | null>(null); // Lock to prevent duplicate attempts
  const connectionTimeoutRef = useRef<any>(null);
  const incomingFilesRef = useRef<{ [key: string]: { meta: FileMeta; chunks: Blob[]; receivedSize: number; startTime: number; lastUpdate: number; bytesSinceLastUpdate: number } }>({});
  const outgoingFilesRef = useRef<{ [key: string]: { startTime: number; lastUpdate: number; bytesSent: number; bytesSinceLastUpdate: number } }>({});
  const handshakeIntervalRef = useRef<any>(null);
  const heartbeatIntervalRef = useRef<any>(null);

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

  // Initialize Peer
  useEffect(() => {
    if (peerRef.current) return; // Prevent double initialization

    const fullId = `${APP_PREFIX}${myId}`;
    
    console.log(`Initializing Peer with ID: ${fullId}`);

    const peer = new Peer(fullId, {
      host: '0.peerjs.com',
      port: 443,
      secure: true,
      debug: 2, // Level 2 for more insights
      pingInterval: 5000, // Keep mobile connections alive
      config: {
        // Standard Google STUN is most reliable.
        // We avoid adding too many servers to prevent timeouts.
        iceServers: [
          { urls: 'stun:stun.l.google.com:19302' }
        ],
        sdpSemantics: 'unified-plan'
      },
    });

    peer.on('open', (id: string) => {
      console.log('Peer connection open. ID:', id);
      setIsPeerReady(true);
      setError(null);
    });

    peer.on('disconnected', () => {
      console.log("Disconnected from signaling server. P2P connections may still persist.");
      setIsPeerReady(false);
      
      // Auto-reconnect to signaling server if connection drops
      if (peerRef.current && !peerRef.current.destroyed) {
        setTimeout(() => {
          if (peerRef.current && !peerRef.current.destroyed && peerRef.current.disconnected) {
            console.log("Attempting to reconnect to signaling server...");
            peerRef.current.reconnect();
          }
        }, 3000);
      }
    });

    peer.on('connection', (conn: any) => {
      console.log("Incoming connection from:", conn.peer);
      
      if (connectingToRef.current && connectingToRef.current !== conn.peer) {
        console.warn("Received connection while attempting another. Switching to incoming.");
        // Cancel outgoing attempt
        if (connectionTimeoutRef.current) clearTimeout(connectionTimeoutRef.current);
        setIsConnecting(false);
        connectingToRef.current = null;
      }
      
      handleConnection(conn);
    });

    peer.on('error', (err: any) => {
      console.warn("Peer Error:", err.type, err.message);

      // If we are connecting, handle specific errors to cancel the loading state
      if (isConnecting) {
        if (err.type === 'peer-unavailable') {
          if (connectionTimeoutRef.current) clearTimeout(connectionTimeoutRef.current);
          setIsConnecting(false);
          connectingToRef.current = null;
          setError(`Device ID not found. Ensure the other device is open and connected to internet.`);
          return;
        }
      }

      // Ignore background network noise
      if (err.type === 'network' || err.message === 'Lost connection to server.') {
        if (isConnecting) {
          setError('Signaling connection lost. Please check internet.');
          setIsConnecting(false);
          connectingToRef.current = null;
        }
        return;
      }

      if (err.type === 'unavailable-id') {
         setError('ID Collision. Refresh to get a new ID.');
      } else if (err.type === 'browser-incompatible') {
        setError('Browser incompatible. Please use Chrome, Firefox or Safari.');
      }
    });

    peerRef.current = peer;

    return () => {
      // Cleanup handled by window unload usually
    };
  }, [myId]);

  // Logic to connect to a specific ID
  const connectToId = (targetShortId: string) => {
    if (!targetShortId || !peerRef.current) return;
    
    const formattedId = targetShortId.toUpperCase();
    const targetFullId = `${APP_PREFIX}${formattedId}`;

    if (formattedId === myId) {
      setError("You cannot connect to yourself.");
      return;
    }

    if (peerRef.current.disconnected) {
       console.log("Peer disconnected, reconnecting before call...");
       peerRef.current.reconnect();
    }

    if (connectingToRef.current === targetFullId) return;

    // Cleanup previous
    if (connRef.current) {
      connRef.current.close();
    }

    setIsConnecting(true);
    setIceState('checking');
    setError(null);
    connectingToRef.current = targetFullId;
    
    console.log("Attempting to connect to:", targetFullId);

    try {
      // CRITICAL FIX: Removed 'reliable: true'. 
      // Reliable mode often fails on mobile hotspots/strict NATs.
      // Browser default (ordered) is sufficient and more robust.
      const conn = peerRef.current.connect(targetFullId);
      
      connectionTimeoutRef.current = setTimeout(() => {
        if (!conn.open) {
          console.warn("Connection timed out for:", targetFullId);
          conn.close();
          setIsConnecting(false);
          connectingToRef.current = null;
          setError("Connection timed out. Firewalls might be blocking the direct path.");
        }
      }, 30000); 

      conn.on('open', () => {
        if (connectionTimeoutRef.current) clearTimeout(connectionTimeoutRef.current);
        connectingToRef.current = null;
        handleConnection(conn);
      });

      conn.on('error', (err: any) => {
        console.error("Connection error:", err);
        if (connectionTimeoutRef.current) clearTimeout(connectionTimeoutRef.current);
        setIsConnecting(false);
        connectingToRef.current = null;
        setError("Failed to establish connection.");
      });

      conn.on('close', () => {
        if (connectingToRef.current === targetFullId) {
             setIsConnecting(false);
             connectingToRef.current = null;
        }
      });

    } catch (e) {
      console.error("Immediate connection error:", e);
      setIsConnecting(false);
      connectingToRef.current = null;
      setError("Could not initiate connection.");
    }
  };

  // Auto-Connect Effect
  useEffect(() => {
    if (!isPeerReady || connectedPeer || isConnecting) return;

    const params = new URLSearchParams(window.location.search);
    const connectTo = params.get('connect');

    if (connectTo && connectTo.length === 4) {
      const target = `${APP_PREFIX}${connectTo.toUpperCase()}`;
      if (connectingToRef.current === target) return;

      console.log("Auto-connecting to ID from URL:", connectTo);
      setConnectionInput(connectTo.toUpperCase());
      window.history.replaceState({}, '', window.location.pathname);
      connectToId(connectTo);
    }
  }, [isPeerReady, connectedPeer, isConnecting]);


  const handleConnection = (conn: any) => {
    if (connRef.current && connRef.current !== conn) {
      connRef.current.close();
    }
    connRef.current = conn;

    // Monitor ICE State
    if (conn.peerConnection) {
      conn.peerConnection.oniceconnectionstatechange = () => {
        const state = conn.peerConnection.iceConnectionState;
        console.log(`ICE State (${conn.peer}):`, state);
        setIceState(state);
      };
    }

    const finalize = () => {
      console.log("Connection established with:", conn.peer);
      setIsConnecting(false);
      connectingToRef.current = null;
      setError(null);
      setIceState('connected');
      
      if (handshakeIntervalRef.current) clearInterval(handshakeIntervalRef.current);
      
      // Aggressive Handshake
      handshakeIntervalRef.current = setInterval(() => {
        if (conn.open) {
           try {
             conn.send({
               type: MessageType.HANDSHAKE,
               payload: { name: displayName }
             });
           } catch (e) {
             console.error("Handshake send error:", e);
           }
        }
      }, 500);
      
      if (heartbeatIntervalRef.current) clearInterval(heartbeatIntervalRef.current);
      heartbeatIntervalRef.current = setInterval(() => {
        if(conn.open) {
           // Keep NAT alive
           try { conn.send({ type: 'PING' }); } catch(e) {}
        }
      }, 4000);
    };

    if (conn.open) {
        finalize();
    } else {
        conn.on('open', finalize);
    }

    conn.on('data', (data: PeerMessage | any) => {
      // Handle PING or Data
      if (data?.type === 'PING') return;
      
      handleData(data);
    });

    conn.on('close', () => {
      console.log("Connection closed");
      if (handshakeIntervalRef.current) clearInterval(handshakeIntervalRef.current);
      if (heartbeatIntervalRef.current) clearInterval(heartbeatIntervalRef.current);
      setConnectedPeer(null);
      connRef.current = null;
      setIsConnecting(false);
      setIceState('closed');
      setTransfers(prev => prev.map(t => t.status === 'transferring' ? { ...t, status: 'error' } : t));
    });
  };

  const handleConnectSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    connectToId(connectionInput);
  };

  const handleData = (message: PeerMessage) => {
    if (handshakeIntervalRef.current) {
        clearInterval(handshakeIntervalRef.current);
        handshakeIntervalRef.current = null;
    }

    if (!message || !message.type) return;

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
          if (now - fileContext.lastUpdate > 500 || fileContext.receivedSize >= fileContext.meta.size) {
            const progress = Math.min(100, (fileContext.receivedSize / fileContext.meta.size) * 100);
            
            const timeDiff = (now - fileContext.lastUpdate) / 1000;
            const speedBytes = fileContext.bytesSinceLastUpdate / (timeDiff || 0.5);
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

          if (fileContext.receivedSize >= fileContext.meta.size) {
            const blob = new Blob(fileContext.chunks, { type: fileContext.meta.type });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileContext.meta.name;
            a.click();
            setTimeout(() => URL.revokeObjectURL(url), 60000);

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

    try {
      connRef.current.send({
        type: MessageType.FILE_META,
        payload: {
          id: fileId,
          name: file.name,
          size: file.size,
          type: file.type
        } as FileMeta
      });
    } catch (e) {
      console.error("Failed to send meta:", e);
      setTransfers(prev => prev.map(t => t.id === fileId ? { ...t, status: 'error' } : t));
      return;
    }

    let offset = 0;
    const reader = new FileReader();

    const sendNextChunk = () => {
      if (!connRef.current || !connRef.current.open) {
        setTransfers(prev => prev.map(t => t.id === fileId ? { ...t, status: 'error' } : t));
        return;
      }

      // Basic Backpressure
      if (connRef.current.dataChannel?.bufferedAmount > 10 * 1024 * 1024) {
        setTimeout(sendNextChunk, 50);
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
          setTransfers(prev => prev.map(t => t.id === fileId ? { ...t, status: 'error' } : t));
          return;
        }

        offset += chunk.byteLength;
        
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
          if (offset % (CHUNK_SIZE * 5) === 0) {
             setTimeout(sendNextChunk, 0);
          } else {
             sendNextChunk();
          }
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
          <div className={`flex items-center gap-2 text-sm px-3 py-1 rounded-full border ${isOnline ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-amber-500/10 border-amber-500/30 text-amber-400'}`}>
            {isOnline ? <Wifi size={14} /> : <WifiOff size={14} />}
            <span className="hidden sm:inline">{isOnline ? 'Signaling Server Online' : 'Offline'}</span>
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
          if (handshakeIntervalRef.current) clearInterval(handshakeIntervalRef.current);
          setConnectedPeer(null);
          setTransfers([]);
          setConnectionInput('');
          setIceState('new');
        }}
      />

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-200 p-4 rounded-xl mb-8 flex items-start gap-3 animate-in fade-in slide-in-from-top-2">
          <AlertTriangle size={20} className="mt-0.5 flex-shrink-0" />
          <div className="flex-1">
             <p className="font-medium">{error}</p>
             {(error.includes("timed out") || error.includes("Failed to establish")) && (
                <div className="text-sm mt-2 bg-red-500/20 p-3 rounded text-red-100">
                  <p className="font-semibold mb-1">Hotspot Connection Guide:</p>
                  <ul className="list-disc list-inside space-y-1 opacity-90">
                    <li><strong>Host Phone:</strong> Turn OFF Mobile Data while waiting for connection.</li>
                    <li><strong>Client Laptop:</strong> Ensure you are connected to the Phone's Wi-Fi.</li>
                    <li>Try connecting in the reverse direction (Enter Laptop ID into Phone).</li>
                    <li>Disable VPNs on both devices.</li>
                  </ul>
                </div>
             )}
          </div>
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
              <form onSubmit={handleConnectSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Peer ID</label>
                  <input
                    type="text"
                    value={connectionInput}
                    onChange={(e) => setConnectionInput(e.target.value.toUpperCase())}
                    placeholder="E.G. X9Y2"
                    disabled={isConnecting}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-lg uppercase tracking-wider disabled:opacity-50"
                    maxLength={4}
                  />
                </div>
                <Button 
                  type="submit" 
                  fullWidth 
                  disabled={!connectionInput || connectionInput.length < 4 || (!isOnline && !peerRef.current?.open) || isConnecting}
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
              
              {isConnecting && (iceState === 'checking' || iceState === 'new') && (
                 <div className="mt-4 p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
                   <div className="flex items-center gap-2 text-blue-300 text-xs mb-1">
                     <Loader2 size={12} className="animate-spin" />
                     <span>Negotiating Local Path...</span>
                   </div>
                   <p className="text-[10px] text-slate-400">
                     Checking LAN/Wi-Fi routes. If this hangs, try disabling Mobile Data on the host phone.
                   </p>
                 </div>
              )}
              
              {isConnecting && iceState === 'disconnected' && (
                <div className="mt-4 p-3 bg-amber-500/10 rounded-lg border border-amber-500/20 text-xs text-amber-300">
                  Direct path failed. Retrying...
                </div>
              )}

              <div className="mt-6 pt-6 border-t border-slate-700/50">
                <div className="flex items-start gap-3 text-xs text-slate-500">
                  <Info size={16} className="flex-shrink-0 mt-0.5" />
                  <p>Internet is only used for the initial handshake. Files are transferred directly over Wi-Fi.</p>
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