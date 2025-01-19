import { Card, CardContent, CardMedia, Typography, Box, Chip, Rating, Icon } from '@mui/material';
import { Course } from '../../types/api';
import { Link } from 'react-router-dom';

interface CourseCardProps {
  course: Course;
}

const CourseCard = ({ course }: CourseCardProps) => {
  return (
    <Card
      component={Link}
      to={`/courses/${course.id}`}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        textDecoration: 'none',
        borderRadius: 2,
        overflow: 'hidden',
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 12px 24px rgba(0,0,0,0.1)',
        },
      }}
    >
      <CardMedia
        component="img"
        height="200"
        image={course.thumbnail || '/placeholder-course.jpg'}
        alt={course.title}
        sx={{ objectFit: 'cover' }}
      />
      <CardContent sx={{ flexGrow: 1, p: 2.5 }}>
        <Box sx={{ mb: 2 }}>
          <Chip
            label={course.category?.name || 'Общее'}
            size="small"
            sx={{
              bgcolor: 'rgba(219,67,55,0.1)',
              color: '#DB4337',
              fontWeight: 500,
              mb: 1,
            }}
          />
          <Typography
            variant="h6"
            component="h3"
            sx={{
              fontWeight: 600,
              fontSize: '1.1rem',
              mb: 1,
              color: '#242424',
              lineHeight: 1.4,
            }}
          >
            {course.title}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              mb: 2,
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
              lineHeight: 1.5,
            }}
          >
            {course.description}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
          <Rating value={course.rating || 0} readOnly size="small" sx={{ mr: 1 }} />
          <Typography variant="body2" color="text.secondary">
            ({course.reviews_count || 0})
          </Typography>
        </Box>

        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderTop: '1px solid',
            borderColor: 'divider',
            pt: 2,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', color: 'text.secondary' }}>
            <Icon sx={{ fontSize: '1rem', mr: 0.5 }}>schedule</Icon>
            <Typography variant="body2">{course.duration || '2ч 30м'}</Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', color: 'text.secondary' }}>
            <Icon sx={{ fontSize: '1rem', mr: 0.5 }}>group</Icon>
            <Typography variant="body2">{course.students_count || 0}</Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export { CourseCard };
