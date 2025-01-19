import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import Home from '../Home';
import { api } from '../../services/api';

// Мокаем API
jest.mock('../../services/api');

// Мокаем компоненты
jest.mock('../../components/Home/Hero', () => () => <div data-testid="hero">Hero Component</div>);
jest.mock('../../components/Home/CategoryList', () => () => <div data-testid="categories">Categories</div>);
jest.mock('../../components/Home/FeatureSection', () => () => <div data-testid="features">Features</div>);
jest.mock('../../components/Home/TestimonialSection', () => () => <div data-testid="testimonials">Testimonials</div>);
jest.mock('../../components/Home/PartnersSection', () => () => <div data-testid="partners">Partners</div>);

const mockCourses = [
  {
    id: 1,
    title: 'Курс 1',
    description: 'Описание курса 1',
    price: 1000,
    image: 'course1.jpg',
    rating: 4.5,
  },
  {
    id: 2,
    title: 'Курс 2',
    description: 'Описание курса 2',
    price: 2000,
    image: 'course2.jpg',
    rating: 5,
  },
];

describe('Home компонент', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    (api.get as jest.Mock).mockReset();
  });

  const renderHome = () => {
    return render(
      <HelmetProvider>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <Home />
          </BrowserRouter>
        </QueryClientProvider>
      </HelmetProvider>
    );
  };

  it('отображает все секции главной страницы', () => {
    renderHome();
    
    expect(screen.getByTestId('hero')).toBeInTheDocument();
    expect(screen.getByTestId('categories')).toBeInTheDocument();
    expect(screen.getByTestId('features')).toBeInTheDocument();
    expect(screen.getByTestId('testimonials')).toBeInTheDocument();
    expect(screen.getByTestId('partners')).toBeInTheDocument();
  });

  it('отображает популярные курсы после загрузки', async () => {
    (api.get as jest.Mock).mockResolvedValueOnce({ data: mockCourses });
    
    renderHome();
    
    // Проверяем заголовок
    expect(screen.getByText('Популярные курсы')).toBeInTheDocument();
    
    // Проверяем загрузку курсов
    const course1 = await screen.findByText('Курс 1');
    const course2 = await screen.findByText('Курс 2');
    
    expect(course1).toBeInTheDocument();
    expect(course2).toBeInTheDocument();
  });

  it('отображает скелетон во время загрузки курсов', () => {
    (api.get as jest.Mock).mockImplementationOnce(() => new Promise(() => {}));
    
    renderHome();
    
    const skeletons = screen.getAllByTestId('skeleton');
    expect(skeletons).toHaveLength(6);
  });

  it('правильно вызывает API для получения популярных курсов', () => {
    renderHome();
    
    expect(api.get).toHaveBeenCalledWith('/api/v1/courses/courses/popular/');
  });
});
