import { Button } from '@/components/kit/Button/Button';
import { Input } from '@/components/kit/Input/Input';
import { Card } from '@/components/kit/Card/Card';
import { Modal } from '@/components/kit/Modal/Modal';
import { Canvas } from '@/components/kit/Canvas/Canvas';
import { Node } from '@/components/kit/Node/Node';
import { Connection } from '@/components/kit/Connection/Connection';

export const Resolver = {
  Button,
  Input,
  Card,
  Modal,
  Canvas,
  Node,
  Connection,
} as const;

export type ResolverComponents = typeof Resolver;