import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { vi } from 'vitest';
import CategoryList from '../CategoryList';
import { api } from '../../../services/api';

// Мокаем модуль api
vi.mock('../../../services/api', () => ({
  api: {
    get: vi.fn(),
  },
}));

const mockCategories = {
  results: [
    {
      id: 1,
      name: 'Программирование',
      description: 'Курсы по программированию',
      icon: 'code',
    },
    {
      id: 2,
      name: 'Бизнес',
      description: 'Бизнес курсы',
      icon: 'business',
    },
  ],
};

describe('CategoryList', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    // Очищаем моки перед каждым тестом
    vi.clearAllMocks();
  });

  const renderComponent = () => {
    return render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <CategoryList />
        </MemoryRouter>
      </QueryClientProvider>
    );
  };

  it('отображает заголовок "Категории курсов"', () => {
    renderComponent();
    expect(screen.getByText('Категории курсов')).toBeInTheDocument();
  });

  it('отображает скелетон при загрузке', () => {
    renderComponent();
    const skeletons = screen.getAllByTestId('skeleton');
    expect(skeletons).toHaveLength(4);
  });

  it('отображает список категорий после загрузки', async () => {
    // Мокаем успешный ответ API
    (api.get as any).mockResolvedValueOnce({ data: mockCategories });

    renderComponent();

    // Ждем, пока категории загрузятся
    await waitFor(() => {
      expect(screen.getByText('Программирование')).toBeInTheDocument();
      expect(screen.getByText('Бизнес')).toBeInTheDocument();
    });

    // Проверяем, что API был вызван с правильными параметрами
    expect(api.get).toHaveBeenCalledWith('/courses/categories/');
  });

  it('корректно обрабатывает ошибки при загрузке', async () => {
    // Мокаем ошибку API
    (api.get as any).mockRejectedValueOnce(new Error('Failed to fetch'));

    renderComponent();

    // Проверяем, что компонент не упал с ошибкой
    await waitFor(() => {
      expect(screen.getByText('Категории курсов')).toBeInTheDocument();
    });
  });

  it('создает правильные ссылки для категорий', async () => {
    (api.get as any).mockResolvedValueOnce({ data: mockCategories });

    renderComponent();

    // Ждем, пока категории загрузятся
    await waitFor(() => {
      const links = screen.getAllByRole('link');
      expect(links[0]).toHaveAttribute('href', '/courses?category=1');
      expect(links[1]).toHaveAttribute('href', '/courses?category=2');
    });
  });
});
