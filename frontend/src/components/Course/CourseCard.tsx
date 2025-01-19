import { Card, CardContent, CardMedia, Typography, Box, Rating, Button, Chip } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { Course } from '../../types/api';

interface CourseCardProps {
  course: Course;
}

const CourseCard = ({ course }: CourseCardProps) => {
  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        transition: 'transform 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
        },
      }}
    >
      <CardMedia
        component="img"
        height="140"
        image={`https://source.unsplash.com/random/400x200/?education,${course.title}`}
        alt={course.title}
      />
      <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ mb: 1 }}>
          <Chip 
            label={course.category.name} 
            size="small" 
            sx={{ mr: 1, mb: 1 }} 
          />
          <Chip 
            label={course.difficulty_level} 
            size="small" 
            color="secondary" 
            sx={{ mb: 1 }} 
          />
        </Box>
        
        <Typography gutterBottom variant="h6" component="h2" sx={{ mb: 1 }}>
          {course.title}
        </Typography>
        
        <Typography 
          variant="body2" 
          color="text.secondary" 
          sx={{ 
            mb: 2,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
          }}
        >
          {course.description}
        </Typography>

        <Box sx={{ mt: 'auto' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Rating value={course.rating} precision={0.5} readOnly size="small" />
            <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
              ({course.reviews_count})
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6" color="primary">
              {course.course_type === 'free' ? 'Бесплатно' : `${course.price} сом`}
            </Typography>
            <Button 
              component={RouterLink} 
              to={`/courses/${course.slug}`}
              variant="contained" 
              size="small"
            >
              Подробнее
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export { CourseCard };
