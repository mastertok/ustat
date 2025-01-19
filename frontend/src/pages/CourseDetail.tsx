import { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  Button,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemText,
  Rating,
  Avatar,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  useTheme,
  useMediaQuery,
  Skeleton,
} from '@mui/material';
import {
  Favorite,
  FavoriteBorder,
  ExpandMore,
  PlayCircleOutline,
  School,
  AccessTime,
  Language,
  Lock,
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { Course, Review } from '../types/api';
import { formatPrice } from '../utils/format';
import SEO from '../components/Shared/SEO';

const CourseDetail = () => {
  const { id } = useParams<{ id: string }>();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [selectedModule, setSelectedModule] = useState<number | null>(null);
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { data: course, isLoading } = useQuery<Course>({
    queryKey: ['course', id],
    queryFn: async () => {
      const response = await api.get(`/courses/${id}/`);
      return response.data;
    },
  });

  const toggleFavorite = useMutation({
    mutationFn: async () => {
      const response = await api.post(`/courses/${id}/toggle_favorite/`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['course', id]);
    },
  });

  const enroll = useMutation({
    mutationFn: async () => {
      const response = await api.post(`/courses/${id}/enroll/`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['course', id]);
    },
  });

  const submitReview = useMutation({
    mutationFn: async (reviewData: Partial<Review>) => {
      const response = await api.post(`/courses/${id}/review/`, reviewData);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['course', id]);
    },
  });

  if (isLoading) {
    return (
      <Box sx={{ py: 4 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            <Grid item xs={12} md={8}>
              <Skeleton variant="rectangular" height={400} sx={{ borderRadius: 2, mb: 4 }} />
              <Skeleton variant="text" height={60} sx={{ mb: 2 }} />
              <Skeleton variant="rectangular" height={200} sx={{ borderRadius: 2 }} />
            </Grid>
            <Grid item xs={12} md={4}>
              <Skeleton variant="rectangular" height={300} sx={{ borderRadius: 2 }} />
            </Grid>
          </Grid>
        </Container>
      </Box>
    );
  }

  if (!course) {
    navigate('/404');
    return null;
  }

  // Подготавливаем ключевые слова для SEO
  const keywords = [
    course.title,
    course.category.name,
    'онлайн курс',
    'обучение',
    course.level,
    course.language === 'ru' ? 'русский язык' : course.language === 'kg' ? 'кыргызский язык' : 'английский язык',
    'Устат',
    'образование',
    'онлайн образование',
    course.instructor.first_name,
    course.instructor.last_name,
  ].join(', ');

  return (
    <>
      <SEO
        title={course.meta_title || course.title}
        description={course.meta_description || course.description.slice(0, 160)}
        keywords={course.meta_keywords || keywords}
        image={course.image}
        type="article"
        author={`${course.instructor.first_name} ${course.instructor.last_name}`}
      />

      <Box sx={{ py: 4 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {/* Левая колонка */}
            <Grid item xs={12} md={8}>
              {/* Заголовок и превью */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h1" sx={{ 
                  fontSize: { xs: '2rem', md: '2.5rem' },
                  fontWeight: 600,
                  mb: 2,
                }}>
                  {course.title}
                </Typography>
                
                {course.preview_video ? (
                  <Box
                    sx={{
                      position: 'relative',
                      paddingTop: '56.25%', // 16:9
                      backgroundColor: 'black',
                      borderRadius: 2,
                      overflow: 'hidden',
                      mb: 2,
                    }}
                  >
                    <iframe
                      style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        border: 0,
                      }}
                      src={course.preview_video}
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                      title={`Превью курса ${course.title}`}
                    />
                  </Box>
                ) : (
                  <Box
                    component="img"
                    src={course.image}
                    alt={course.title}
                    sx={{
                      width: '100%',
                      borderRadius: 2,
                      mb: 2,
                    }}
                  />
                )}
              </Box>

              {/* Описание курса */}
              <Card sx={{ mb: 4 }}>
                <CardContent>
                  <Typography variant="h5" gutterBottom component="h2">
                    О курсе
                  </Typography>
                  <Typography 
                    variant="body1" 
                    color="text.secondary" 
                    sx={{ whiteSpace: 'pre-line' }}
                    component="div"
                  >
                    {course.description}
                  </Typography>
                </CardContent>
              </Card>

              {/* Содержание курса */}
              <Card sx={{ mb: 4 }}>
                <CardContent>
                  <Typography variant="h5" gutterBottom component="h2">
                    Содержание курса
                  </Typography>
                  {course.modules.map((module) => (
                    <Accordion
                      key={module.id}
                      expanded={selectedModule === module.id}
                      onChange={() => setSelectedModule(selectedModule === module.id ? null : module.id)}
                    >
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                          <Typography sx={{ flexGrow: 1 }}>{module.title}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {module.lessons_count} уроков
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        <List disablePadding>
                          {module.lessons.map((lesson) => (
                            <ListItem
                              key={lesson.id}
                              sx={{
                                borderBottom: `1px solid ${theme.palette.divider}`,
                                '&:last-child': { borderBottom: 0 },
                              }}
                            >
                              <ListItemText
                                primary={
                                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                    {lesson.is_free ? (
                                      <PlayCircleOutline sx={{ mr: 1 }} />
                                    ) : (
                                      <Lock sx={{ mr: 1 }} />
                                    )}
                                    {lesson.title}
                                  </Box>
                                }
                                secondary={lesson.duration}
                              />
                            </ListItem>
                          ))}
                        </List>
                      </AccordionDetails>
                    </Accordion>
                  ))}
                </CardContent>
              </Card>

              {/* Отзывы */}
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h5" sx={{ flexGrow: 1 }} component="h2">
                      Отзывы студентов
                    </Typography>
                    <Rating value={course.average_rating} readOnly precision={0.5} />
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                      ({course.reviews.length})
                    </Typography>
                  </Box>

                  <List>
                    {course.reviews.map((review) => (
                      <ListItem
                        key={review.id}
                        sx={{
                          display: 'block',
                          borderBottom: `1px solid ${theme.palette.divider}`,
                          '&:last-child': { borderBottom: 0 },
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Avatar sx={{ mr: 2 }}>{review.user.first_name[0]}</Avatar>
                          <Box sx={{ flexGrow: 1 }}>
                            <Typography variant="subtitle1">
                              {review.user.first_name} {review.user.last_name}
                            </Typography>
                            <Rating value={review.rating} readOnly size="small" />
                          </Box>
                          <Typography variant="body2" color="text.secondary">
                            {new Date(review.created_at).toLocaleDateString()}
                          </Typography>
                        </Box>
                        <Typography variant="body1">{review.comment}</Typography>
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>

            {/* Правая колонка */}
            <Grid item xs={12} md={4}>
              <Box sx={{ position: 'sticky', top: 24 }}>
                {/* Карточка с ценой и кнопками */}
                <Card sx={{ mb: 4 }}>
                  <CardContent>
                    <Typography variant="h4" sx={{ mb: 2 }}>
                      {formatPrice(course.price)}
                    </Typography>

                    <Button
                      variant="contained"
                      color="primary"
                      fullWidth
                      size="large"
                      onClick={() => enroll.mutate()}
                      disabled={course.is_enrolled}
                      sx={{ mb: 2 }}
                    >
                      {course.is_enrolled ? 'Вы уже записаны' : 'Записаться на курс'}
                    </Button>

                    <Button
                      variant="outlined"
                      color="primary"
                      fullWidth
                      size="large"
                      startIcon={course.is_favorite ? <Favorite /> : <FavoriteBorder />}
                      onClick={() => toggleFavorite.mutate()}
                      sx={{ mb: 2 }}
                    >
                      {course.is_favorite ? 'В избранном' : 'Добавить в избранное'}
                    </Button>

                    <Divider sx={{ my: 2 }} />

                    <List disablePadding>
                      <ListItem disablePadding sx={{ mb: 1 }}>
                        <School sx={{ mr: 2 }} />
                        <ListItemText
                          primary="Уровень"
                          secondary={course.level}
                        />
                      </ListItem>
                      <ListItem disablePadding sx={{ mb: 1 }}>
                        <AccessTime sx={{ mr: 2 }} />
                        <ListItemText
                          primary="Длительность"
                          secondary={course.duration}
                        />
                      </ListItem>
                      <ListItem disablePadding>
                        <Language sx={{ mr: 2 }} />
                        <ListItemText
                          primary="Язык"
                          secondary={course.language === 'ru' ? 'Русский' : course.language === 'kg' ? 'Кыргызский' : 'Английский'}
                        />
                      </ListItem>
                    </List>
                  </CardContent>
                </Card>

                {/* Информация о преподавателе */}
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom component="h2">
                      Преподаватель
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar
                        sx={{ width: 64, height: 64, mr: 2 }}
                        src={`https://ui-avatars.com/api/?name=${encodeURIComponent(
                          `${course.instructor.first_name} ${course.instructor.last_name}`
                        )}&size=64`}
                        alt={`${course.instructor.first_name} ${course.instructor.last_name}`}
                      />
                      <Box>
                        <Typography variant="subtitle1">
                          {course.instructor.first_name} {course.instructor.last_name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {course.instructor.email}
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </>
  );
};

export default CourseDetail;
