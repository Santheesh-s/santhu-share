export enum MessageType {
  HANDSHAKE = 'HANDSHAKE',
  FILE_META = 'FILE_META',
  FILE_CHUNK = 'FILE_CHUNK',
  FILE_ACK = 'FILE_ACK',
}

export interface PeerMessage {
  type: MessageType;
  payload: any;
}

export interface FileMeta {
  id: string;
  name: string;
  size: number;
  type: string;
}

export interface FileProgress {
  id: string;
  fileName: string;
  fileSize: number;
  progress: number; // 0 to 100
  direction: 'incoming' | 'outgoing';
  status: 'pending' | 'transferring' | 'completed' | 'error';
  blobParts?: Blob[]; // For incoming files
  speed?: string;
}

export interface PeerConnectionData {
  connectionId: string;
  displayName: string;
  conn: any; // PeerJS DataConnection
}

// 64KB chunks are generally good for WebRTC
export const CHUNK_SIZE = 64 * 1024;