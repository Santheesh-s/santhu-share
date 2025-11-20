import React from 'react';
import { File, ArrowUp, ArrowDown, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { FileProgress } from '../types';
import { formatBytes } from '../utils/formatters';

interface FileTransferItemProps {
  transfer: FileProgress;
}

export const FileTransferItem: React.FC<FileTransferItemProps> = ({ transfer }) => {
  const isIncoming = transfer.direction === 'incoming';
  const isCompleted = transfer.status === 'completed';
  const isError = transfer.status === 'error';

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex items-center gap-4 shadow-sm transition-all hover:border-slate-600">
      {/* Icon Status */}
      <div className={`h-12 w-12 rounded-lg flex items-center justify-center flex-shrink-0 ${
        isError ? 'bg-red-500/20 text-red-400' :
        isCompleted ? 'bg-emerald-500/20 text-emerald-400' :
        'bg-blue-500/20 text-blue-400'
      }`}>
        {isError ? <XCircle size={20} /> :
         isCompleted ? <CheckCircle size={20} /> :
         isIncoming ? <ArrowDown size={20} className="animate-bounce" /> : <ArrowUp size={20} className="animate-bounce" />}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-1">
          <h4 className="font-medium text-white truncate pr-4">{transfer.fileName}</h4>
          <span className="text-xs font-medium text-slate-400 flex-shrink-0">
            {formatBytes(transfer.fileSize)}
          </span>
        </div>

        {/* Progress Bar */}
        <div className="h-2 w-full bg-slate-700 rounded-full overflow-hidden relative">
          <div 
            className={`h-full transition-all duration-300 ease-out ${
              isCompleted ? 'bg-emerald-500' : 
              isError ? 'bg-red-500' : 
              'bg-blue-500'
            }`}
            style={{ width: `${transfer.progress}%` }}
          >
             {!isCompleted && !isError && (
               <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
             )}
          </div>
        </div>
        
        <div className="flex justify-between mt-1.5">
          <div className="flex gap-2">
             <span className="text-xs text-slate-500">
               {isCompleted ? 'Completed' : isError ? 'Failed' : isIncoming ? 'Receiving...' : 'Sending...'}
             </span>
             {transfer.speed && !isCompleted && !isError && (
               <span className="text-xs font-mono text-emerald-400 font-medium">
                 {transfer.speed}
               </span>
             )}
          </div>
          <span className="text-xs font-mono text-slate-500">
            {Math.round(transfer.progress)}%
          </span>
        </div>
      </div>
    </div>
  );
};