interface MicroburbsLogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  showText?: boolean
  textSize?: string
}

const sizeMap = {
  sm: 'h-6 w-6',
  md: 'h-7 w-7',
  lg: 'h-9 w-9',
  xl: 'h-16 w-16'
}

const textSizeMap = {
  sm: 'text-base',
  md: 'text-lg',
  lg: 'text-2xl',
  xl: 'text-5xl'
}

export function MicroburbsLogo({ size = 'md', showText = true, textSize }: MicroburbsLogoProps) {
  const displayTextSize = textSize || textSizeMap[size]
  
  return (
    <div className="inline-flex items-center gap-2 justify-center">
      <svg 
        className={sizeMap[size]} 
        viewBox="0 0 100 100" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* House body */}
        <rect x="20" y="35" width="60" height="50" className="fill-primary" rx="2"/>
        {/* Roof */}
        <path d="M50 15 L80 35 L20 35 Z" className="fill-primary"/>
        {/* Door */}
        <rect x="35" y="50" width="12" height="20" fill="white"/>
        {/* Window */}
        <rect x="53" y="50" width="12" height="12" fill="white"/>
      </svg>
      {showText && (
        <span className={`${displayTextSize} font-semibold text-primary whitespace-nowrap`}>
          Microburbs
        </span>
      )}
    </div>
  )
}

