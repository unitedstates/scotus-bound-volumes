# scotus-bound-volumes

The official publication of the Supreme Court is the [bound volumes of the United States Reports](http://www.supremecourt.gov/opinions/boundvolumes.aspx). On the Supreme Court's website, there are PDFs of the bound volumes dating from 1991.

There are a couple of problems with these bound volumes: 

1. They're old. The [most recent one](http://www.supremecourt.gov/opinions/boundvolumes/557bv.pdf) is from the 2008 term.
2. They're PDFs. Large (several hundred page) unstructured PDFs.

There are a couple of *great* things about these bound volumes:

1. They have all of the cases from a given term AND all of the orders from the term.
2. They come with some small data sets near the end.
3. They have a hand-rolled index at the very end.
4. In some situations, they have touching little artifacts about the Court (such as the recent retirement letters of Justice Souter).

So, the goal is to parse up these PDFs and make some beautiful XML/HTML. A word of caution, though, based on an earlier effort on my part. Because there are headers, footers, and footnotes, it is insufficient to simply `pdftotext` the bound volumes. Some clustering will likely be needed. With that, let's begin.