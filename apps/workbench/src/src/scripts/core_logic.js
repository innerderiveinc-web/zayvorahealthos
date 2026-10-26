const locOrigin = (typeof window !== 'undefined' && window.location && window.location.origin && window.location.origin !== 'null')
      ? window.location.origin
      : ((typeof window !== 'undefined' && window.location && window.location.protocol && window.location.host) ? window.location.protocol + '//' + window.location.host : '');
    const API_BASE = (locOrigin.includes('localhost') || locOrigin.includes('127.0.0.1'))
      ? locOrigin
      : (window.ZMIE_BACKEND_URL || locOrigin || '');
    window.API_BASE = API_BASE;
