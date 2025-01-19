import { Box, Container, Typography } from '@mui/material';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay } from 'swiper/modules';
import 'swiper/css';

const partners = [
  {
    name: 'Google',
    logo: '/images/partners/google.png',
  },
  {
    name: 'Microsoft',
    logo: '/images/partners/microsoft.png',
  },
  {
    name: 'Amazon',
    logo: '/images/partners/amazon.png',
  },
  {
    name: 'IBM',
    logo: '/images/partners/ibm.png',
  },
  {
    name: 'Oracle',
    logo: '/images/partners/oracle.png',
  },
  {
    name: 'Intel',
    logo: '/images/partners/intel.png',
  },
];

const PartnersSection = () => {
  return (
    <Box sx={{ py: 8, bgcolor: 'background.default' }}>
      <Container>
        <Typography
          component="h2"
          variant="h3"
          align="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Наши партнеры
        </Typography>

        <Swiper
          modules={[Autoplay]}
          spaceBetween={30}
          slidesPerView={2}
          autoplay={{
            delay: 2500,
            disableOnInteraction: false,
          }}
          loop={true}
          breakpoints={{
            640: {
              slidesPerView: 3,
            },
            768: {
              slidesPerView: 4,
            },
            1024: {
              slidesPerView: 5,
            },
          }}
        >
          {partners.map((partner) => (
            <SwiperSlide key={partner.name}>
              <Box
                sx={{
                  height: 100,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  filter: 'grayscale(100%)',
                  opacity: 0.7,
                  transition: 'all 0.3s',
                  '&:hover': {
                    filter: 'grayscale(0%)',
                    opacity: 1,
                  },
                }}
              >
                <Box
                  component="img"
                  src={partner.logo}
                  alt={partner.name}
                  sx={{
                    maxWidth: '80%',
                    maxHeight: '80%',
                    objectFit: 'contain',
                  }}
                />
              </Box>
            </SwiperSlide>
          ))}
        </Swiper>
      </Container>
    </Box>
  );
};

export default PartnersSection;
