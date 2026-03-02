import { Component } from 'react'

export default class ErrorBoundary extends Component {
  state = { hasError: false, error: null }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    console.error('ErrorBoundary:', error, info)
  }

  render() {
    if (this.state.hasError) {
      const Fallback = this.props.fallback
      if (typeof Fallback === 'function') return <Fallback error={this.state.error} />
      return (
        <div className="error-boundary-fallback">
          <p>Something went wrong displaying this section.</p>
          {this.props.showRetry && (
            <button type="button" onClick={() => this.setState({ hasError: false, error: null })}>
              Try again
            </button>
          )}
        </div>
      )
    }
    return this.props.children
  }
}
