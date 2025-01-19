import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Container,
  Grid,
  Typography,
  Tabs,
  Tab,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Skeleton,
} from '@mui/material';
import { CourseCard } from '../components/Course/CourseCard';
import { api } from '../services/api';
import { Course } from '../types/api';
import SEO from '../components/Shared/SEO';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`profile-tabpanel-${index}`}
      aria-labelledby={`profile-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

const Profile = () => {
  const [tabValue, setTabValue] = useState(0);

  const { data: enrolledCourses, isLoading: isLoadingEnrolled } = useQuery<Course[]>({
    queryKey: ['enrolledCourses'],
    queryFn: async () => {
      const response = await api.get('/api/v1/courses/enrolled/');
      return response.data;
    },
  });

  const { data: favoriteCourses, isLoading: isLoadingFavorites } = useQuery<Course[]>({
    queryKey: ['favoriteCourses'],
    queryFn: async () => {
      const response = await api.get('/api/v1/courses/favorites/');
      return response.data;
    },
  });

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box sx={{ py: 4 }}>
      <SEO
        title="Мой профиль | Устат"
        description="Управляйте своими курсами и настройками"
        keywords="профиль, курсы, обучение"
      />
      
      <Container>
        <Typography variant="h3" component="h1" gutterBottom>
          Мой профиль
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Мои курсы" />
            <Tab label="Избранное" />
            <Tab label="Настройки" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={4}>
            {isLoadingEnrolled
              ? [...Array(6)].map((_, index) => (
                  <Grid item key={index} xs={12} sm={6} md={4}>
                    <Skeleton variant="rectangular" height={320} />
                  </Grid>
                ))
              : enrolledCourses?.map((course) => (
                  <Grid item key={course.id} xs={12} sm={6} md={4}>
                    <CourseCard course={course} />
                  </Grid>
                ))}
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={4}>
            {isLoadingFavorites
              ? [...Array(6)].map((_, index) => (
                  <Grid item key={index} xs={12} sm={6} md={4}>
                    <Skeleton variant="rectangular" height={320} />
                  </Grid>
                ))
              : favoriteCourses?.map((course) => (
                  <Grid item key={course.id} xs={12} sm={6} md={4}>
                    <CourseCard course={course} />
                  </Grid>
                ))}
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Личные данные
              </Typography>
              <List>
                <ListItem>
                  <ListItemText primary="Email" secondary="user@example.com" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Имя" secondary="Иван Иванов" />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Дата регистрации" secondary="01.01.2024" />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </TabPanel>
      </Container>
    </Box>
  );
};

export default Profile;
