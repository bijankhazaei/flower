import { useCallback, useEffect } from 'react';
import { useCanvasStore } from '@/store/canvasStore';

export const useCanvasInteractions = () => {
  const { 
    zoom, 
    pan, 
    mode, 
    setZoom, 
    setPan, 
    setMode,
    clearSelection,
    deleteNode,
    selection 
  } = useCanvasStore();

  // Zoom with mouse wheel
  const handleWheel = useCallback((e: WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    setZoom(zoom + delta);
  }, [zoom, setZoom]);

  // Pan with middle mouse or space+drag
  const handlePan = useCallback((e: MouseEvent) => {
    if (e.button === 1 || (e.button === 0 && mode === 'pan')) {
      e.preventDefault();
      const startX = e.clientX;
      const startY = e.clientY;
      const startPan = { ...pan };

      const handleMouseMove = (e: MouseEvent) => {
        const deltaX = (e.clientX - startX) / zoom;
        const deltaY = (e.clientY - startY) / zoom;
        setPan({
          x: startPan.x + deltaX,
          y: startPan.y + deltaY
        });
      };

      const handleMouseUp = () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };

      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }
  }, [pan, zoom, mode, setPan]);

  // Keyboard shortcuts
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.target instanceof HTMLInputElement) return;

    switch (e.key) {
      case 'Delete':
      case 'Backspace':
        selection.forEach(nodeId => deleteNode(nodeId));
        break;
      case 'Escape':
        clearSelection();
        setMode('select');
        break;
      case ' ':
        e.preventDefault();
        setMode('pan');
        break;
      case '1':
        setZoom(1);
        break;
      case '0':
        setPan({ x: 0, y: 0 });
        break;
    }
  }, [selection, deleteNode, clearSelection, setMode, setZoom, setPan]);

  const handleKeyUp = useCallback((e: KeyboardEvent) => {
    if (e.key === ' ' && mode === 'pan') {
      setMode('select');
    }
  }, [mode, setMode]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('keyup', handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp]);

  return {
    handleWheel,
    handlePan
  };
};