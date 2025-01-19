import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Hero from '../Hero';

// Мок для Swiper
jest.mock('swiper/react', () => ({
  Swiper: ({ children }: { children: React.ReactNode }) => <div data-testid="swiper">{children}</div>,
  SwiperSlide: ({ children }: { children: React.ReactNode }) => <div data-testid="swiper-slide">{children}</div>,
}));

// Мок для стилей Swiper
jest.mock('swiper/css', () => ({}));
jest.mock('swiper/css/effect-fade', () => ({}));
jest.mock('swiper/css/navigation', () => ({}));
jest.mock('swiper/css/pagination', () => ({}));

describe('Hero компонент', () => {
  const renderHero = () => {
    return render(
      <BrowserRouter>
        <Hero />
      </BrowserRouter>
    );
  };

  it('отображает все слайды', () => {
    renderHero();
    const slides = screen.getAllByTestId('swiper-slide');
    expect(slides).toHaveLength(3);
  });

  it('содержит правильные заголовки на каждом слайде', () => {
    renderHero();
    expect(screen.getByText('Устат')).toBeInTheDocument();
    expect(screen.getByText('Учитесь у лучших')).toBeInTheDocument();
    expect(screen.getByText('Удобное обучение')).toBeInTheDocument();
  });

  it('содержит кнопки навигации на каждом слайде', () => {
    renderHero();
    const buttons = screen.getAllByRole('button');
    expect(buttons.length).toBeGreaterThan(0);
  });

  it('имеет правильные подзаголовки', () => {
    renderHero();
    expect(screen.getByText('Онлайн платформа для обучения на кыргызском и русском языках')).toBeInTheDocument();
    expect(screen.getByText('Курсы от ведущих специалистов и экспертов')).toBeInTheDocument();
    expect(screen.getByText('Учитесь в любое время и в любом месте')).toBeInTheDocument();
  });

  it('содержит кнопки с правильным текстом', () => {
    renderHero();
    expect(screen.getByText('Найти курсы')).toBeInTheDocument();
    expect(screen.getByText('Начать обучение')).toBeInTheDocument();
    expect(screen.getByText('Выбрать курс')).toBeInTheDocument();
  });
});
