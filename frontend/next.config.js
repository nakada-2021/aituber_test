
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:8000/api/:path*'
      },
      {
        source: '/audio/:path*',
        destination: 'http://backend:8000/audio/:path*'
      }
    ]
  }
}
