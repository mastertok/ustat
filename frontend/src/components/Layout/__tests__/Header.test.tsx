import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import theme from '../../../theme';
import Header from '../Header';

const renderHeader = () => {
  return render(
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <Header />
      </ThemeProvider>
    </BrowserRouter>
  );
};

describe('Header компонент', () => {
  it('отображает логотип', () => {
    renderHeader();
    const logo = screen.getAllByText('УСТАТ');
    expect(logo).toHaveLength(2); // Десктопный и мобильный логотип
  });

  it('отображает навигационные ссылки', () => {
    renderHeader();
    expect(screen.getByText('Главная')).toBeInTheDocument();
    expect(screen.getByText('Курсы')).toBeInTheDocument();
    expect(screen.getByText('О нас')).toBeInTheDocument();
  });

  it('отображает переключатель языка', () => {
    renderHeader();
    expect(screen.getByText('RU')).toBeInTheDocument();
    expect(screen.getByText('KG')).toBeInTheDocument();
  });

  it('переключает язык при клике', () => {
    renderHeader();
    const kgButton = screen.getByText('KG');
    fireEvent.click(kgButton);
    expect(kgButton.closest('button')).toHaveClass('Mui-selected');
  });

  it('открывает мобильное меню', () => {
    renderHeader();
    const menuButton = screen.getByLabelText('меню навигации');
    fireEvent.click(menuButton);
    expect(screen.getByRole('menu')).toBeInTheDocument();
  });

  it('открывает меню пользователя', () => {
    renderHeader();
    const avatarButton = screen.getByAltText('User Avatar');
    fireEvent.click(avatarButton);
    expect(screen.getByText('Профиль')).toBeInTheDocument();
    expect(screen.getByText('Мои курсы')).toBeInTheDocument();
    expect(screen.getByText('Выйти')).toBeInTheDocument();
  });
});
