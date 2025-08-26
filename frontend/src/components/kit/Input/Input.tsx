import React from 'react';
import { cn } from '@/utilities/helpers';
import { InputProps } from '@/contracts/components';

export const Input: React.FC<InputProps> = ({
  className,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  ...props
}) => {
  return (
    <div className="w-full">
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-dominant-500 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50',
          error && 'border-error-500 focus:ring-error-500',
          className
        )}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-error-600">{error}</p>
      )}
    </div>
  );
};