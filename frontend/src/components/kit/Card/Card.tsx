import React from 'react';
import { cn } from '@/utilities/helpers';
import { CardProps } from '@/contracts/components';

const paddingVariants = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6'
};

export const Card: React.FC<CardProps> = ({
  className,
  children,
  padding = 'md',
  ...props
}) => {
  return (
    <div
      className={cn(
        'rounded-lg border border-gray-200 bg-white shadow-sm',
        paddingVariants[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};