import React, { forwardRef } from 'react';
import { cn } from '@/utilities/helpers';
import { CanvasProps } from '@/contracts/components';

export const Canvas = forwardRef<HTMLDivElement, CanvasProps>(({
  zoom,
  pan,
  mode,
  onCanvasClick,
  children,
  className,
  ...props
}, ref) => {
  return (
    <div
      ref={ref}
      className={cn('relative w-full h-full overflow-hidden bg-gray-50', className)}
      onClick={onCanvasClick}
      {...props}
    >
      {/* Grid background */}
      <div className="absolute inset-0 opacity-20">
        <svg width="100%" height="100%">
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e5e7eb" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>
      
      {/* Canvas content */}
      <div
        className="absolute inset-0"
        style={{
          transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
          transformOrigin: '0 0'
        }}
      >
        {children}
      </div>
    </div>
  );
});

Canvas.displayName = 'Canvas';