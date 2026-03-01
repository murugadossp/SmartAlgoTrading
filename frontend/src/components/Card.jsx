export default function Card({ title, children, onClick, className = '', as: Component = 'div' }) {
  const isButton = Component === 'button'
  const props = {
    className: `card ${onClick && !isButton ? 'card-clickable' : ''} ${className}`.trim(),
    ...(onClick && isButton ? { onClick, type: 'button' } : {}),
    ...(onClick && !isButton ? { role: 'button', tabIndex: 0, onClick, onKeyDown: (e) => e.key === 'Enter' && onClick(e) } : {}),
  }
  return (
    <Component {...props}>
      {title && <h3 className="card-title">{title}</h3>}
      <div className="card-body">{children}</div>
    </Component>
  )
}
