'use client'

import { ReactNode } from 'react'

interface FormFieldProps {
  label: string
  type?: 'text' | 'number' | 'email' | 'url' | 'select' | 'textarea' | 'file' | 'checkbox' | 'slider'
  value: any
  onChange: (value: any) => void
  placeholder?: string
  options?: Array<{ value: string; label: string }>
  min?: number
  max?: number
  step?: number
  disabled?: boolean
  required?: boolean
  error?: string
  helperText?: string
  icon?: ReactNode
}

export function FormField({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  options,
  min,
  max,
  step,
  disabled = false,
  required = false,
  error,
  helperText,
  icon
}: FormFieldProps) {
  const baseClasses = "w-full px-3 py-2 bg-cyber-dark border rounded text-cyber-primary font-mono transition-colors focus:outline-none focus:border-neon-blue"
  const errorClasses = error ? "border-neon-pink" : "border-neon-blue"
  const disabledClasses = disabled ? "opacity-50 cursor-not-allowed" : ""

  const renderInput = () => {
    switch (type) {
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className={`${baseClasses} ${errorClasses} ${disabledClasses}`}
            disabled={disabled}
          >
            {options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        )

      case 'textarea':
        return (
          <textarea
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            className={`${baseClasses} ${errorClasses} ${disabledClasses} min-h-[100px] resize-y`}
            disabled={disabled}
            rows={4}
          />
        )

      case 'slider':
        return (
          <div className="relative">
            <input
              type="range"
              min={min || 0}
              max={max || 100}
              step={step || 1}
              value={value}
              onChange={(e) => onChange(parseInt(e.target.value))}
              className="w-full h-2 bg-cyber-dark rounded-lg appearance-none cursor-pointer"
              style={{
                background: `linear-gradient(to right, #00d9ff 0%, #00d9ff ${((value - (min || 0)) / ((max || 100) - (min || 0))) * 100}%, #1a1a1a ${((value - (min || 0)) / ((max || 100) - (min || 0))) * 100}%, #1a1a1a 100%)`
              }}
              disabled={disabled}
            />
            <div className="absolute left-0 right-0 flex justify-between text-xs text-cyber-light mt-1">
              <span>{min || 0}</span>
              <span className="text-neon-blue font-mono">{value}</span>
              <span>{max || 100}</span>
            </div>
          </div>
        )

      case 'checkbox':
        return (
          <label className="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              checked={value}
              onChange={(e) => onChange(e.target.checked)}
              className="w-5 h-5 bg-cyber-dark border-neon-blue rounded focus:ring-2 focus:ring-neon-blue"
              disabled={disabled}
            />
            {helperText && <span className="text-sm text-cyber-light">{helperText}</span>}
          </label>
        )

      default:
        return (
          <div className="relative">
            {icon && (
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-neon-blue">
                {icon}
              </div>
            )}
            <input
              type={type}
              value={value}
              onChange={(e) => onChange(type === 'number' ? parseInt(e.target.value) || 0 : e.target.value)}
              placeholder={placeholder}
              className={`${baseClasses} ${errorClasses} ${disabledClasses} ${icon ? 'pl-10' : ''}`}
              disabled={disabled}
            />
          </div>
        )
    }
  }

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-cyber-light">
        {label}
        {required && <span className="text-neon-pink ml-1">*</span>}
      </label>
      {renderInput()}
      {error && <p className="text-xs text-neon-pink">{error}</p>}
      {helperText && !error && <p className="text-xs text-cyber-light">{helperText}</p>}
    </div>
  )
}
