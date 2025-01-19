import { render, screen } from '@testing-library/react';
import PartnersSection from '../PartnersSection';

// Мок для Swiper
jest.mock('swiper/react', () => ({
  Swiper: ({ children }: { children: React.ReactNode }) => <div data-testid="swiper">{children}</div>,
  SwiperSlide: ({ children }: { children: React.ReactNode }) => <div data-testid="swiper-slide">{children}</div>,
}));

// Мок для стилей Swiper
jest.mock('swiper/css', () => ({}));

describe('PartnersSection компонент', () => {
  it('отображает заголовок секции', () => {
    render(<PartnersSection />);
    expect(screen.getByText('Наши партнеры')).toBeInTheDocument();
  });

  it('отображает все слайды с партнерами', () => {
    render(<PartnersSection />);
    const slides = screen.getAllByTestId('swiper-slide');
    expect(slides).toHaveLength(6); // Количество партнеров
  });

  it('содержит изображения всех партнеров', () => {
    render(<PartnersSection />);
    const images = screen.getAllByRole('img');
    expect(images).toHaveLength(6);

    // Проверяем alt текст для каждого изображения
    expect(images[0]).toHaveAttribute('alt', 'Google');
    expect(images[1]).toHaveAttribute('alt', 'Microsoft');
    expect(images[2]).toHaveAttribute('alt', 'Amazon');
    expect(images[3]).toHaveAttribute('alt', 'IBM');
    expect(images[4]).toHaveAttribute('alt', 'Oracle');
    expect(images[5]).toHaveAttribute('alt', 'Intel');
  });

  it('имеет правильные пути к изображениям', () => {
    render(<PartnersSection />);
    const images = screen.getAllByRole('img');
    
    images.forEach((img, index) => {
      expect(img).toHaveAttribute('src', expect.stringContaining('/images/partners/'));
    });
  });

  it('содержит слайдер с правильными настройками', () => {
    render(<PartnersSection />);
    const swiper = screen.getByTestId('swiper');
    expect(swiper).toBeInTheDocument();
  });
});
