import { Box, Grid, Typography } from '@mui/material';
import {
  School,
  Devices,
  Assignment,
  GroupWork,
  Timeline,
  EmojiEvents,
} from '@mui/icons-material';

const features = [
  {
    icon: School,
    title: 'Лучшие преподаватели',
    description: 'Учитесь у опытных профессионалов своего дела',
  },
  {
    icon: Devices,
    title: 'Удобный формат',
    description: 'Занимайтесь в любое время с любого устройства',
  },
  {
    icon: Assignment,
    title: 'Практические задания',
    description: 'Закрепляйте знания на реальных проектах',
  },
  {
    icon: GroupWork,
    title: 'Сообщество',
    description: 'Общайтесь и обменивайтесь опытом с другими студентами',
  },
  {
    icon: Timeline,
    title: 'Отслеживание прогресса',
    description: 'Следите за своими достижениями и развитием',
  },
  {
    icon: EmojiEvents,
    title: 'Сертификаты',
    description: 'Получайте подтверждение своих навыков',
  },
];

const FeatureSection = () => {
  return (
    <Box sx={{ py: 8, bgcolor: 'background.default' }}>
      <Box
        sx={{
          width: '100%',
          maxWidth: '100vw',
          px: { xs: 2, sm: 4, md: 6, lg: 8 },
        }}
      >
        <Typography
          component="h2"
          variant="h3"
          align="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Почему выбирают Устат
        </Typography>

        <Grid
          container
          spacing={{ xs: 2, sm: 3, md: 4 }}
          sx={{
            width: '100%',
            margin: 0,
          }}
        >
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Grid item xs={12} sm={6} md={4} key={feature.title}>
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    textAlign: 'center',
                  }}
                >
                  <Box
                    sx={{
                      width: 80,
                      height: 80,
                      borderRadius: '50%',
                      bgcolor: 'primary.main',
                      color: 'white',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 2,
                      transition: 'transform 0.2s',
                      '&:hover': {
                        transform: 'scale(1.1)',
                      },
                    }}
                  >
                    <Icon sx={{ fontSize: 40 }} />
                  </Box>
                  <Typography
                    variant="h6"
                    component="h3"
                    gutterBottom
                    sx={{ color: 'primary.main' }}
                  >
                    {feature.title}
                  </Typography>
                  <Typography
                    variant="body1"
                    color="text.secondary"
                    sx={{ maxWidth: 300 }}
                  >
                    {feature.description}
                  </Typography>
                </Box>
              </Grid>
            );
          })}
        </Grid>
      </Box>
    </Box>
  );
};

export default FeatureSection;
