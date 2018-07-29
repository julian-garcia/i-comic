from django.db import models

class ComicStrip(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.title

class ComicStripFrame(models.Model):
    comic_strip = models.ForeignKey(ComicStrip, on_delete=models.CASCADE)
    narrative = models.TextField()
    image = models.ImageField(upload_to='images')
    sequence = models.IntegerField(null=False, blank=False)
    move = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{0}-{1}: {2}'.format(self.comic_strip.title,
                                     'Frame',
                                     self.frame_number)
