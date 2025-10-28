import { useAuthStore } from '@/store/authStore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, GraduationCap, BookOpen, Calendar, TrendingUp, DollarSign } from 'lucide-react';
import { DashboardLayout } from '@/components/DashboardLayout';

const StatCard = ({ title, value, icon: Icon, description }: any) => (
  <Card>
    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle className="text-sm font-medium">{title}</CardTitle>
      <Icon className="h-4 w-4 text-muted-foreground" />
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
      {description && (
        <p className="text-xs text-muted-foreground mt-1">{description}</p>
      )}
    </CardContent>
  </Card>
);

export default function Dashboard() {
  const { user } = useAuthStore();

  const adminStats = [
    { title: 'Total Students', value: '1,234', icon: Users, description: '+12% from last month' },
    { title: 'Total Faculty', value: '89', icon: GraduationCap, description: '+3 new this month' },
    { title: 'Library Books', value: '5,678', icon: BookOpen, description: '234 currently issued' },
    { title: 'Upcoming Events', value: '12', icon: Calendar, description: '3 this week' },
    { title: 'Fee Collection', value: '$234K', icon: DollarSign, description: '89% collected' },
    { title: 'Attendance Rate', value: '94%', icon: TrendingUp, description: '+2% improvement' },
  ];

  const facultyStats = [
    { title: 'My Students', value: '45', icon: Users, description: 'Across 3 courses' },
    { title: 'Active Courses', value: '3', icon: BookOpen, description: 'This semester' },
    { title: 'Upcoming Events', value: '5', icon: Calendar, description: '2 this week' },
    { title: 'Avg. Attendance', value: '92%', icon: TrendingUp, description: 'Your classes' },
  ];

  const studentStats = [
    { title: 'Current Semester', value: '5', icon: BookOpen, description: '6 courses enrolled' },
    { title: 'Attendance', value: '94%', icon: TrendingUp, description: 'Keep it up!' },
    { title: 'Fee Status', value: 'Paid', icon: DollarSign, description: 'Next due: Dec 31' },
    { title: 'Upcoming Events', value: '8', icon: Calendar, description: '2 registered' },
  ];

  const stats =
    user?.role === 'admin'
      ? adminStats
      : user?.role === 'faculty'
      ? facultyStats
      : studentStats;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Welcome back, {user?.email?.split('@')[0]}!
          </h1>
          <p className="text-muted-foreground">
            {user?.role === 'admin'
              ? 'Here\'s an overview of your university system'
              : user?.role === 'faculty'
              ? 'Here\'s an overview of your courses and students'
              : 'Here\'s an overview of your academic progress'}
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {stats.map((stat) => (
            <StatCard key={stat.title} {...stat} />
          ))}
        </div>

        {user?.role === 'admin' && (
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>Latest updates across the system</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { action: 'New student enrolled', name: 'John Doe', time: '2 hours ago' },
                  { action: 'Book issued', name: 'Introduction to Algorithms', time: '4 hours ago' },
                  { action: 'Fee payment received', name: 'Jane Smith - $5,000', time: '6 hours ago' },
                  { action: 'Event created', name: 'Tech Conference 2024', time: '1 day ago' },
                ].map((activity, i) => (
                  <div key={i} className="flex items-center justify-between border-b last:border-0 pb-3 last:pb-0">
                    <div>
                      <p className="text-sm font-medium">{activity.action}</p>
                      <p className="text-sm text-muted-foreground">{activity.name}</p>
                    </div>
                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
