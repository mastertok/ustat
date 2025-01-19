import { Box, Container, Stack, Typography, Button } from '@mui/material';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import { useEffect, useState } from 'react';

const headerPhrases = [
  'Учитесь у лучших преподавателей',
  'Развивайте свои навыки',
  'Достигайте своих целей',
];

const phrases = [
  'Получите качественное образование и развивайте свои навыки',
  'Станьте востребованным специалистом в своей области',
  'Учитесь у практикующих экспертов онлайн',
  'Развивайте свои профессиональные навыки',
];

const Hero = () => {
  const [currentHeaderIndex, setCurrentHeaderIndex] = useState(0);
  const [displayText, setDisplayText] = useState('');
  const [isVisible, setIsVisible] = useState(true);
  const [isDeleting, setIsDeleting] = useState(false);
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);

  const fullText = 'Онлайн-обучение для вашего профессионального роста';
  const typingSpeed = 50;
  let typingTimeout: ReturnType<typeof setTimeout>;

  useEffect(() => {
    const typeText = () => {
      let currentIndex = 0;
      const type = () => {
        if (currentIndex <= fullText.length) {
          setDisplayText(fullText.slice(0, currentIndex));
          currentIndex++;
          typingTimeout = setTimeout(type, typingSpeed);
        }
      };
      type();
    };

    typeText();

    return () => {
      if (typingTimeout) {
        clearTimeout(typingTimeout);
      }
    };
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsVisible(false);
      setTimeout(() => {
        setCurrentHeaderIndex((prevIndex) =>
          prevIndex === headerPhrases.length - 1 ? 0 : prevIndex + 1
        );
        setIsVisible(true);
      }, 1000);
    }, 8000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let timeout: ReturnType<typeof setTimeout>;
    const currentPhrase = phrases[currentPhraseIndex];

    if (isDeleting) {
      if (displayText === '') {
        setIsDeleting(false);
        setCurrentPhraseIndex((prev) => (prev + 1) % phrases.length);
      } else {
        timeout = setTimeout(() => {
          setDisplayText(displayText.slice(0, -1));
        }, 50);
      }
    } else {
      if (displayText === currentPhrase) {
        timeout = setTimeout(() => {
          setIsDeleting(true);
        }, 2000);
      } else {
        timeout = setTimeout(() => {
          setDisplayText(currentPhrase.slice(0, displayText.length + 1));
        }, 100);
      }
    }

    return () => clearTimeout(timeout);
  }, [displayText, currentPhraseIndex, isDeleting]);

  return (
    <Box
      sx={{
        position: 'relative',
        height: '50vh',
        display: 'flex',
        alignItems: 'center',
        overflow: 'hidden',
        bgcolor: '#f1f1f1',
        borderRadius: '20px',
        mx: 2,
        my: 2,
      }}
    >
      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 2 }}>
        <Stack
          direction={{ xs: 'column', md: 'row' }}
          spacing={4}
          alignItems="center"
          justifyContent="space-between"
        >
          {/* Левая часть с текстом */}
          <Stack spacing={3} maxWidth="600px" position="relative" zIndex={1}>
            <Typography
              variant="h1"
              sx={{
                color: '#DB4337',
                fontWeight: 700,
                fontSize: { xs: '2.5rem', md: '3.5rem' },
                lineHeight: 1.2,
                opacity: isVisible ? 1 : 0,
                transition: 'opacity 1s ease-in-out',
                textShadow: '1px 1px 2px rgba(0,0,0,0.1)',
                letterSpacing: '0.5px',
              }}
            >
              {headerPhrases[currentHeaderIndex]}
            </Typography>
            <Typography
              variant="h5"
              sx={{
                color: '#DB4337',
                fontWeight: 500,
                height: '80px',
                display: 'flex',
                alignItems: 'center',
                letterSpacing: '0.3px',
                textShadow: '1px 1px 2px rgba(0,0,0,0.1)',
                borderRadius: '10px',
                px: 2,
                '&::after': {
                  content: '"|"',
                  marginLeft: '2px',
                  animation: 'blink 1s step-end infinite',
                  color: '#DB4337',
                },
                '@keyframes blink': {
                  'from, to': { opacity: 1 },
                  '50%': { opacity: 0 },
                },
              }}
            >
              {displayText}
            </Typography>
          </Stack>

          {/* Правая часть с блогом */}
          <Box
            sx={{
              position: 'relative',
              zIndex: 1,
              background: 'linear-gradient(45deg, rgba(219,67,55,0.95), rgba(183,28,28,0.95))',
              borderRadius: 2,
              p: 3,
              maxWidth: '400px',
              width: '100%',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
            }}
          >
            <Stack spacing={2}>
              <Stack direction="row" spacing={2} alignItems="center">
                <PlayCircleOutlineIcon sx={{ color: 'white', fontSize: '2rem' }} />
                <Typography variant="h6" sx={{ color: '#ffffff', fontWeight: 600, letterSpacing: '0.3px' }}>
                  Монетизируй свою экспертность
                </Typography>
              </Stack>
              <Typography
                variant="body1"
                sx={{
                  color: '#ffffff',
                  fontSize: '1.1rem',
                  fontWeight: 500,
                  letterSpacing: '0.2px',
                  textShadow: '1px 1px 2px rgba(0,0,0,0.2)',
                }}
              >
                Создавайте курсы, делитесь знаниями и получайте доход
              </Typography>
              <Button
                variant="contained"
                sx={{
                  color: '#1a237e',
                  background: 'linear-gradient(45deg, #ffffff, #f5f5f5)',
                  backgroundSize: '200% 200%',
                  animation: 'gradient-animation 3s linear infinite',
                  fontWeight: 600,
                  px: 4,
                  py: 1.5,
                  fontSize: '1.1rem',
                  border: 'none',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #f5f5f5, #ffffff)',
                    backgroundSize: '200% 200%',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                  },
                }}
              >
                Присоединяйся
              </Button>
            </Stack>
          </Box>
        </Stack>
      </Container>
    </Box>
  );
};

export default Hero;
