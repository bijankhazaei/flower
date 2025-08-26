import { ReactNode, HTMLAttributes, ButtonHTMLAttributes } from 'react';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: ReactNode;
}

export interface InputProps extends HTMLAttributes<HTMLInputElement> {
  type?: 'text' | 'email' | 'password' | 'number';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: string;
}

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  children: ReactNode;
}

export interface CanvasProps extends HTMLAttributes<HTMLDivElement> {
  zoom: number;
  pan: { x: number; y: number };
  mode: 'select' | 'connect' | 'pan' | 'add-node';
  onCanvasClick?: (event: MouseEvent) => void;
  children?: ReactNode;
}

export interface FlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  config: Record<string, any>;
}

export interface NodeProps {
  node: FlowNode;
  isSelected: boolean;
  onDrag?: (offset: { x: number; y: number }) => void;
  onClick?: (nodeId: string) => void;
}

export interface Connection {
  id: string;
  source: string;
  target: string;
  sourcePort?: string;
  targetPort?: string;
}

export interface ConnectionProps {
  connection: Connection;
  nodes: Record<string, FlowNode>;
}