import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, BookOpen, BookCheck } from 'lucide-react';
import { api } from '@/lib/api';
import { toast } from 'sonner';

interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  copies: number;
}

interface Issue {
  student: string;
  book: string;
  issue_date: string;
  return_date: string;
  actual_return_date: string | null;
}

export default function Library() {
  const [books, setBooks] = useState<Book[]>([]);
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchLibraryData();
  }, []);

  const fetchLibraryData = async () => {
    try {
      const [booksRes, issuesRes] = await Promise.all([
        api.get('/admin/library/books'),
        api.get('/admin/library/issues'),
      ]);
      setBooks(booksRes.data);
      setIssues(issuesRes.data);
    } catch (error) {
      toast.error('Failed to fetch library data');
    } finally {
      setLoading(false);
    }
  };

  const filteredBooks = books.filter((book) =>
    book.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    book.author?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    book.isbn?.includes(searchTerm)
  );

  const activeIssues = issues.filter((issue) => !issue.actual_return_date);
  const returnedIssues = issues.filter((issue) => issue.actual_return_date);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Library Management</h1>
            <p className="text-muted-foreground">Manage books and track issues</p>
          </div>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Add Book
          </Button>
        </div>

        <Tabs defaultValue="books" className="space-y-4">
          <TabsList>
            <TabsTrigger value="books">
              <BookOpen className="h-4 w-4 mr-2" />
              Books Catalog
            </TabsTrigger>
            <TabsTrigger value="issues">
              <BookCheck className="h-4 w-4 mr-2" />
              Book Issues
            </TabsTrigger>
          </TabsList>

          <TabsContent value="books" className="space-y-4">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Book Catalog</CardTitle>
                    <CardDescription>Complete library collection</CardDescription>
                  </div>
                  <div className="relative">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search books..."
                      className="pl-8 w-[300px]"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex justify-center py-8">
                    <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
                  </div>
                ) : (
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>ID</TableHead>
                          <TableHead>Title</TableHead>
                          <TableHead>Author</TableHead>
                          <TableHead>ISBN</TableHead>
                          <TableHead>Available Copies</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {filteredBooks.length === 0 ? (
                          <TableRow>
                            <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                              No books found
                            </TableCell>
                          </TableRow>
                        ) : (
                          filteredBooks.map((book) => (
                            <TableRow key={book.id}>
                              <TableCell className="font-medium">{book.id}</TableCell>
                              <TableCell className="font-medium">{book.title}</TableCell>
                              <TableCell>{book.author}</TableCell>
                              <TableCell className="font-mono text-sm">{book.isbn}</TableCell>
                              <TableCell>
                                <Badge
                                  variant={book.copies > 0 ? 'default' : 'destructive'}
                                >
                                  {book.copies} available
                                </Badge>
                              </TableCell>
                            </TableRow>
                          ))
                        )}
                      </TableBody>
                    </Table>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="issues" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Active Issues</CardTitle>
                  <CardDescription>Books currently issued to students</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {activeIssues.length === 0 ? (
                      <p className="text-center text-muted-foreground py-4">No active issues</p>
                    ) : (
                      activeIssues.map((issue, i) => (
                        <div key={i} className="flex items-start justify-between border-b last:border-0 pb-3 last:pb-0">
                          <div className="space-y-1">
                            <p className="font-medium">{issue.book}</p>
                            <p className="text-sm text-muted-foreground">{issue.student}</p>
                            <p className="text-xs text-muted-foreground">
                              Due: {new Date(issue.return_date).toLocaleDateString()}
                            </p>
                          </div>
                          <Button size="sm" variant="outline">Return</Button>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Returned Books</CardTitle>
                  <CardDescription>Recently returned books</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {returnedIssues.slice(0, 5).length === 0 ? (
                      <p className="text-center text-muted-foreground py-4">No returns yet</p>
                    ) : (
                      returnedIssues.slice(0, 5).map((issue, i) => (
                        <div key={i} className="border-b last:border-0 pb-3 last:pb-0">
                          <p className="font-medium">{issue.book}</p>
                          <p className="text-sm text-muted-foreground">{issue.student}</p>
                          <p className="text-xs text-success">
                            Returned: {new Date(issue.actual_return_date!).toLocaleDateString()}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
