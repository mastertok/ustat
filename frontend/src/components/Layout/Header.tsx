import { useState, useEffect } from 'react';
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Container,
  Avatar,
  Button,
  Tooltip,
  MenuItem,
  useTheme,
  useMediaQuery,
  ToggleButton,
  ToggleButtonGroup,
  useScrollTrigger,
  Stack,
} from '@mui/material';
import { Menu as MenuIcon, Language } from '@mui/icons-material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { keyframes } from '@mui/system';

// Анимации
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const pulse = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
`;

const shimmer = keyframes`
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
`;

interface NavItem {
  title: string;
  path: string;
}

const navItems: NavItem[] = [
  { title: 'Главная', path: '/' },
  { title: 'Курсы', path: '/courses' },
  { title: 'О нас', path: '/about' },
];

const userMenuItems: NavItem[] = [
  { title: 'Профиль', path: '/profile' },
  { title: 'Мои курсы', path: '/profile?tab=courses' },
  { title: 'Избранное', path: '/profile?tab=favorites' },
  { title: 'Настройки', path: '/profile?tab=settings' },
];

type Language = 'ru' | 'kg';

const Header = () => {
  const [anchorElNav, setAnchorElNav] = useState<null | HTMLElement>(null);
  const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);
  const [language, setLanguage] = useState<Language>('ru');
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const location = useLocation();

  // Отслеживание прокрутки
  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 100,
  });

  const handleLanguageChange = (
    _: React.MouseEvent<HTMLElement>,
    newLanguage: Language,
  ) => {
    if (newLanguage !== null) {
      setLanguage(newLanguage);
    }
  };

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };
  
  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
    <AppBar 
      position="fixed" 
      sx={{ 
        width: '100%',
        backgroundColor: trigger ? 'rgba(255, 255, 255, 0.98)' : 'background.paper',
        backdropFilter: 'blur(8px)',
        boxShadow: trigger ? '0 2px 8px rgba(0,0,0,0.1)' : '0 1px 3px rgba(0,0,0,0.05)',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        animation: `${fadeIn} 0.5s ease-out`,
      }}
    >
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* Логотип для десктопа */}
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontWeight: 700,
              color: 'primary.main',
              textDecoration: 'none',
              letterSpacing: '.1rem',
              position: 'relative',
              '&:hover': {
                animation: `${pulse} 1s ease-in-out infinite`,
              },
              '&::after': {
                content: '""',
                position: 'absolute',
                bottom: -2,
                left: 0,
                width: '100%',
                height: 2,
                background: 'linear-gradient(90deg, transparent, primary.main, transparent)',
                backgroundSize: '200% 100%',
                animation: `${shimmer} 2s infinite linear`,
              },
            }}
          >
            УСТАТ
          </Typography>

          {/* Мобильное меню */}
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="меню навигации"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="primary"
              sx={{
                '&:hover': {
                  transform: 'rotate(180deg)',
                  transition: 'transform 0.3s ease-in-out',
                },
              }}
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
                '& .MuiPaper-root': {
                  borderRadius: 2,
                  mt: 1.5,
                  overflow: 'visible',
                  filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.15))',
                  '&:before': {
                    content: '""',
                    display: 'block',
                    position: 'absolute',
                    top: 0,
                    left: 14,
                    width: 10,
                    height: 10,
                    bgcolor: 'background.paper',
                    transform: 'translateY(-50%) rotate(45deg)',
                    zIndex: 0,
                  },
                },
              }}
            >
              {navItems.map((item) => (
                <MenuItem
                  key={item.path}
                  onClick={handleCloseNavMenu}
                  component={RouterLink}
                  to={item.path}
                  selected={location.pathname === item.path}
                  sx={{
                    transition: 'all 0.2s ease-in-out',
                    '&:hover': {
                      transform: 'translateX(8px)',
                      backgroundColor: 'primary.light',
                    },
                  }}
                >
                  <Typography textAlign="center">{item.title}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>

          {/* Логотип для мобильных */}
          <Typography
            variant="h5"
            noWrap
            component={RouterLink}
            to="/"
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontWeight: 700,
              color: 'primary.main',
              textDecoration: 'none',
              letterSpacing: '.1rem',
              '&:hover': {
                animation: `${pulse} 1s ease-in-out infinite`,
              },
            }}
          >
            УСТАТ
          </Typography>

          {/* Десктопное меню */}
          <Stack
            direction="row"
            spacing={4}
            alignItems="center"
            justifyContent="center"
            sx={{ flex: 1 }}
          >
            {navItems.map((item) => (
              <Button
                key={item.path}
                component={RouterLink}
                to={item.path}
                onClick={handleCloseNavMenu}
                sx={{
                  my: 2,
                  mx: 1,
                  color: location.pathname === item.path ? 'primary.main' : 'text.primary',
                  display: 'block',
                  fontWeight: location.pathname === item.path ? 700 : 400,
                  position: 'relative',
                  transition: 'all 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    color: 'primary.main',
                  },
                  '&::after': {
                    content: '""',
                    position: 'absolute',
                    bottom: 0,
                    left: 12,
                    width: location.pathname === item.path ? 'calc(100% - 24px)' : '0%',
                    height: 2,
                    background: (theme) => theme.palette.primary.main,
                    transition: 'all 0.3s ease-in-out',
                    borderRadius: 1,
                  },
                  '&:hover::after': {
                    width: 'calc(100% - 24px)',
                  },
                }}
              >
                {item.title}
              </Button>
            ))}
          </Stack>

          {/* Переключатель языка */}
          <Box sx={{ mr: 2 }}>
            <ToggleButtonGroup
              value={language}
              exclusive
              onChange={handleLanguageChange}
              aria-label="язык"
              size="small"
              sx={{
                '& .MuiToggleButton-root': {
                  px: 2,
                  py: 0.5,
                  color: 'text.primary',
                  transition: 'all 0.3s ease-in-out',
                  '&.Mui-selected': {
                    color: '#ffffff',
                    background: (theme) => `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                    backgroundSize: '200% 200%',
                    animation: `${shimmer} 3s linear infinite`,
                    '&:hover': {
                      background: (theme) => `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                      backgroundSize: '200% 200%',
                      opacity: 0.9,
                    },
                  },
                  '&:hover': {
                    transform: 'translateY(-2px)',
                  },
                },
              }}
            >
              <ToggleButton 
                value="ru" 
                aria-label="русский"
                sx={{ 
                  borderRadius: '4px 0 0 4px',
                  textTransform: 'none',
                }}
              >
                RU
              </ToggleButton>
              <ToggleButton 
                value="kg" 
                aria-label="кыргызча"
                sx={{ 
                  borderRadius: '0 4px 4px 0',
                  textTransform: 'none',
                }}
              >
                KG
              </ToggleButton>
            </ToggleButtonGroup>
          </Box>

          {/* Меню пользователя */}
          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Открыть настройки">
              <IconButton 
                onClick={handleOpenUserMenu} 
                sx={{ 
                  p: 0,
                  transition: 'transform 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'scale(1.1)',
                  },
                }}
              >
                <Avatar 
                  alt="User Avatar" 
                  src="/images/avatar.jpg"
                  sx={{
                    border: '2px solid transparent',
                    background: (theme) => `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main}) border-box`,
                  }}
                />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ 
                mt: '45px',
                '& .MuiPaper-root': {
                  borderRadius: 2,
                  mt: 1.5,
                  overflow: 'visible',
                  filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.15))',
                  '&:before': {
                    content: '""',
                    display: 'block',
                    position: 'absolute',
                    top: 0,
                    right: 14,
                    width: 10,
                    height: 10,
                    bgcolor: 'background.paper',
                    transform: 'translateY(-50%) rotate(45deg)',
                    zIndex: 0,
                  },
                },
              }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              {userMenuItems.map((item) => (
                <MenuItem
                  key={item.path}
                  onClick={handleCloseUserMenu}
                  component={RouterLink}
                  to={item.path}
                  sx={{
                    transition: 'all 0.2s ease-in-out',
                    '&:hover': {
                      transform: 'translateX(8px)',
                      backgroundColor: 'primary.light',
                    },
                  }}
                >
                  <Typography textAlign="center">{item.title}</Typography>
                </MenuItem>
              ))}
              <MenuItem 
                onClick={handleCloseUserMenu}
                sx={{
                  transition: 'all 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateX(8px)',
                    backgroundColor: 'error.light',
                  },
                }}
              >
                <Typography textAlign="center" color="error">Выйти</Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;
