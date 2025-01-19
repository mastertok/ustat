import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  ru: {
    translation: {
      hero: {
        title: 'Учитесь у лучших экспертов',
        subtitle: 'Получите качественное образование и развивайте свои навыки',
        startLearning: 'Начать обучение',
        latestBlog: 'Последний видеоблог',
        blogPreview: 'Узнайте о последних трендах в образовании и развитии',
        watchNow: 'Смотреть сейчас'
      }
    }
  },
  kg: {
    translation: {
      hero: {
        title: 'Мыкты эксперттерден үйрөнүңүз',
        subtitle: 'Сапаттуу билим алыңыз жана көндүмдөрүңүздү өнүктүрүңүз',
        startLearning: 'Окууну баштоо',
        latestBlog: 'Акыркы видеоблог',
        blogPreview: 'Билим берүү жана өнүгүү тармагындагы акыркы тенденциялар жөнүндө билиңиз',
        watchNow: 'Азыр көрүү'
      }
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'ru',
    fallbackLng: 'ru',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
