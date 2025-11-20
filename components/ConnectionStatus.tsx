import React, { useState } from 'react';
import { Wifi, User, Copy, Share2, Check, RefreshCw, Globe, ToggleLeft, ToggleRight } from 'lucide-react';
import { Button } from './Button';

interface ConnectionStatusProps {
  myId: string;
  displayName: string;
  connectedTo?: string;
  connectedPeerName?: string;
  onDisconnect: () => void;
  onReset?: () => void;
  lanMode?: boolean;
  onToggleLanMode?: () => void;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({
  myId,
  displayName,
  connectedTo,
  connectedPeerName,
  onDisconnect,
  onReset,
  lanMode,
  onToggleLanMode
}) => {
  const [copied, setCopied] = useState(false);
  const [shared, setShared] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(myId);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const shareLink = async () => {
    if (!myId) return;
    const url = `${window.location.origin}${window.location.pathname}?connect=${myId}`;
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Connect to AirShare P2P',
          text: `Connect to ${displayName} to share files securely.`,
          url: url
        });
        setShared(true);
      } catch (err) {
        console.log('Error sharing:', err);
        // Fallback to clipboard if user cancelled or failed
      }
    } else {
      // Desktop Fallback
      navigator.clipboard.writeText(url);
      setShared(true);
    }
    
    setTimeout(() => setShared(false), 2000);
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-md border border-slate-700 rounded-2xl p-6 mb-8">
      <div className="flex flex-col md:flex-row justify-between items-center gap-6">
        
        {/* My Identity */}
        <div className="flex items-center gap-4 w-full md:w-auto">
          <div className="h-12 w-12 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 flex-shrink-0">
            <User size={24} />
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase tracking-wider font-semibold">You are</p>
            <h3 className="text-lg font-bold text-white">{displayName}</h3>
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              <span className="text-sm text-slate-400">ID: <span className="font-mono text-blue-300">{myId || '...'}</span></span>
              <button onClick={copyToClipboard} className="text-slate-500 hover:text-slate-300 transition-colors p-1" title="Copy ID">
                {copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
              </button>
              
              {!connectedTo && myId && (
                 <button 
                   onClick={shareLink} 
                   className="flex items-center gap-1 text-xs bg-blue-600/20 text-blue-300 px-2 py-1 rounded hover:bg-blue-600/30 transition-colors ml-2"
                 >
                   {shared ? <Check size={12} /> : <Share2 size={12} />}
                   {shared ? 'Link Sent' : 'Share Link'}
                 </button>
              )}
            </div>
          </div>
        </div>

        {/* Connection Indicator */}
        <div className="flex flex-col items-center gap-3">
          <div className="flex items-center gap-3 px-4 py-2 rounded-full bg-slate-900/50 border border-slate-700">
            <div className={`h-3 w-3 rounded-full animate-pulse ${connectedTo ? 'bg-emerald-500' : 'bg-amber-500'}`} />
            <span className="text-sm font-medium text-slate-300">
              {connectedTo ? 'Connected via LAN/P2P' : 'Waiting for connection...'}
            </span>
          </div>
          
          <div className="flex gap-4 items-center">
             {onReset && !connectedTo && (
                <button onClick={onReset} className="text-[10px] text-slate-500 flex items-center gap-1 hover:text-blue-400 transition-colors">
                  <RefreshCw size={10} /> Reset Network
                </button>
             )}
             
             {onToggleLanMode && !connectedTo && (
                <button onClick={onToggleLanMode} className={`text-[10px] flex items-center gap-1 transition-colors ${lanMode ? 'text-emerald-400 font-semibold' : 'text-slate-500 hover:text-slate-300'}`} title="Enable if using Mobile Hotspot">
                  {lanMode ? <ToggleRight size={16} /> : <ToggleLeft size={16} />}
                  <span>{lanMode ? 'Hotspot Mode' : 'Standard Mode'}</span>
                </button>
             )}
          </div>
        </div>

        {/* Connected Peer Info */}
        {connectedTo && (
          <div className="flex items-center gap-4 w-full md:w-auto justify-end">
             <div className="text-right">
              <p className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Connected to</p>
              <h3 className="text-lg font-bold text-white">{connectedPeerName || 'Unknown Device'}</h3>
            </div>
            <div className="h-12 w-12 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 flex-shrink-0">
              <Wifi size={24} />
            </div>
            <Button variant="secondary" onClick={onDisconnect} className="ml-2 !px-3">
              Disconnect
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};