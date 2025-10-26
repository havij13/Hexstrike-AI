'use client'

import { useState, InputHTMLAttributes } from 'react'
import { AlertCircle, CheckCircle2 } from 'lucide-react'

interface ValidationRule {
  validate: (value: string) => boolean
  message: string
}

interface ValidatedInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string
  validationRules?: ValidationRule[]
  showSuccess?: boolean
}

export function ValidatedInput({
  label,
  validationRules = [],
  showSuccess = false,
  className = '',
  ...props
}: ValidatedInputProps) {
  const [value, setValue] = useState(props.defaultValue || '')
  const [errors, setErrors] = useState<string[]>([])
  const [isValid, setIsValid] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value
    setValue(newValue)

    if (validationRules.length === 0) {
      setIsValid(true)
      setErrors([])
      props.onChange?.(e)
      return
    }

    const newErrors: string[] = []
    for (const rule of validationRules) {
      if (!rule.validate(newValue)) {
        newErrors.push(rule.message)
      }
    }

    setErrors(newErrors)
    setIsValid(newErrors.length === 0 && newValue.length > 0)
    props.onChange?.(e)
  }

  const hasError = errors.length > 0
  const showValidation = String(value).length > 0 && validationRules.length > 0

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-cyber-light">
        {label}
        {props.required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div className="relative">
        <input
          {...props}
          value={value}
          onChange={handleChange}
          className={`
            w-full px-4 py-2 bg-cyber-dark border-2 rounded-lg
            text-cyber-light placeholder:text-cyber-light/50
            focus:outline-none focus:ring-2 focus:ring-neon-blue/50
            transition-all duration-200
            ${hasError ? 'border-red-500 focus:border-red-500' : ''}
            ${showValidation && isValid && !hasError ? 'border-green-500 focus:border-green-500' : ''}
            ${!hasError && !showValidation ? 'border-cyber-primary' : ''}
            ${className}
          `}
        />
        
        {/* Validation Icons */}
        {showValidation && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            {hasError ? (
              <AlertCircle className="h-5 w-5 text-red-500" />
            ) : isValid && showSuccess ? (
              <CheckCircle2 className="h-5 w-5 text-green-500" />
            ) : null}
          </div>
        )}
      </div>

      {/* Error Messages */}
      {hasError && (
        <div className="space-y-1">
          {errors.map((error, index) => (
            <p key={index} className="text-sm text-red-400 flex items-center gap-1">
              <AlertCircle className="h-4 w-4" />
              {error}
            </p>
          ))}
        </div>
      )}
    </div>
  )
}

// Common validation rules
export const validationRules = {
  required: (message = 'This field is required'): ValidationRule => ({
    validate: (value) => value.trim().length > 0,
    message
  }),
  
  minLength: (length: number, message?: string): ValidationRule => ({
    validate: (value) => value.length >= length,
    message: message || `Must be at least ${length} characters`
  }),
  
  maxLength: (length: number, message?: string): ValidationRule => ({
    validate: (value) => value.length <= length,
    message: message || `Must be no more than ${length} characters`
  }),
  
  url: (message = 'Must be a valid URL'): ValidationRule => ({
    validate: (value) => {
      try {
        new URL(value)
        return true
      } catch {
        return false
      }
    },
    message
  }),
  
  ipAddress: (message = 'Must be a valid IP address'): ValidationRule => ({
    validate: (value) => {
      const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/
      if (!ipRegex.test(value)) return false
      return value.split('.').every(octet => parseInt(octet) <= 255)
    },
    message
  }),
  
  email: (message = 'Must be a valid email address'): ValidationRule => ({
    validate: (value) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(value)
    },
    message
  }),
  
  port: (message = 'Must be a valid port number (1-65535)'): ValidationRule => ({
    validate: (value) => {
      const port = parseInt(value)
      return !isNaN(port) && port >= 1 && port <= 65535
    },
    message
  }),
  
  noSpaces: (message = 'Cannot contain spaces'): ValidationRule => ({
    validate: (value) => !value.includes(' '),
    message
  })
}
