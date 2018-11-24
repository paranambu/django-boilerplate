import Cookies from 'js-cookie'
import i18next from 'i18next'

import es from './es/translation.json'

export default i18next
  .init({
    debug: 'production' !== process.env.NODE_ENV,
    lng: Cookies.get('language_code') || 'en',
    returnEmptyString: false,
    resources: {
      es: {translation: es}
    }
  })
