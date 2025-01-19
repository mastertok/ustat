import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';
import TestimonialSection from '../TestimonialSection';
import { api } from '../../../services/api';

// Мокаем модуль api
vi.mock('../../../services/api', () => ({
  api: {
    get: vi.fn(),
  },
}));

const mockReviews = {
  results: [
    {
      id: 1,
      user: {
        id: 1,
        username: 'user1',
        first_name: 'Иван',
        last_name: 'Иванов',
        email: 'ivan@example.com',
      },
      course: {
        id: 1,
        title: 'Python для начинающих',
      },
      rating: 5,
      comment: 'Отличный курс!',
      created_at: '2024-01-19T10:00:00Z',
    },
    {
      id: 2,
      user: {
        id: 2,
        username: 'user2',
        first_name: 'Петр',
        last_name: 'Петров',
        email: 'petr@example.com',
      },
      course: {
        id: 2,
        title: 'JavaScript Продвинутый',
      },
      rating: 4,
      comment: 'Очень полезный курс',
      created_at: '2024-01-19T11:00:00Z',
    },
    {
      id: 3,
      user: {
        id: 3,
        username: 'user3',
        first_name: 'Анна',
        last_name: 'Сидорова',
        email: 'anna@example.com',
      },
      course: {
        id: 3,
        title: 'React Мастер',
      },
      rating: 5,
      comment: 'Супер курс!',
      created_at: '2024-01-19T12:00:00Z',
    },
  ],
};

describe('TestimonialSection', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    vi.clearAllMocks();
  });

  const renderComponent = () => {
    return render(
      <QueryClientProvider client={queryClient}>
        <TestimonialSection />
      </QueryClientProvider>
    );
  };

  it('отображает заголовок "Отзывы наших студентов"', () => {
    renderComponent();
    expect(screen.getByText('Отзывы наших студентов')).toBeInTheDocument();
  });

  it('отображает скелетон при загрузке', () => {
    renderComponent();
    const skeletons = screen.getAllByRole('generic').filter(
      element => element.className.includes('MuiSkeleton-root')
    );
    expect(skeletons).toHaveLength(2);
  });

  it('отображает отзывы после загрузки', async () => {
    (api.get as any).mockResolvedValueOnce({ data: mockReviews });

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Отличный курс!')).toBeInTheDocument();
      expect(screen.getByText('Очень полезный курс')).toBeInTheDocument();
    });

    expect(screen.getByText('Иван Иванов')).toBeInTheDocument();
    expect(screen.getByText('Python для начинающих')).toBeInTheDocument();
  });

  it('корректно обрабатывает навигацию по отзывам', async () => {
    (api.get as any).mockResolvedValueOnce({ data: mockReviews });

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText('Отличный курс!')).toBeInTheDocument();
    });

    // Проверяем, что кнопка "назад" изначально отключена
    const prevButton = screen.getByRole('button', { name: /назад/i });
    expect(prevButton).toBeDisabled();

    // Нажимаем кнопку "вперед"
    const nextButton = screen.getByRole('button', { name: /вперед/i });
    fireEvent.click(nextButton);

    // Проверяем, что отображаются следующие отзывы
    await waitFor(() => {
      expect(screen.getByText('Супер курс!')).toBeInTheDocument();
    });

    // Проверяем, что теперь кнопка "назад" активна
    expect(prevButton).not.toBeDisabled();
  });

  it('корректно обрабатывает ошибки при загрузке', async () => {
    (api.get as any).mockRejectedValueOnce(new Error('Failed to fetch'));

    renderComponent();

    // Проверяем, что компонент не упал с ошибкой
    await waitFor(() => {
      expect(screen.getByText('Отзывы наших студентов')).toBeInTheDocument();
    });
  });

  it('делает правильный API запрос', async () => {
    (api.get as any).mockResolvedValueOnce({ data: mockReviews });

    renderComponent();

    expect(api.get).toHaveBeenCalledWith('/reviews/reviews/', {
      params: {
        rating__gte: 4,
        ordering: '-created_at',
        limit: 10,
      },
    });
  });
});
