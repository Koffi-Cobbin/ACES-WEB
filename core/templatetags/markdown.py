from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
import markdown2
import re

from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension

register = template.Library()


@register.filter(name="markdown")
@stringfilter
def markdown(value):
    generated_html = markdown2.markdown(value, extras=['fenced-code-blocks', 'code-color', 'extra', "footnotes"])
    return mark_safe(f"<div class='markdown'>{generated_html}</div>")


@register.filter(name="unmarkdown")
@stringfilter
def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = md.markdown(markdown_string, extensions=['fenced_code', CodeHiliteExtension(pygments_style='native', linenos=False), 'extra', "footnotes"])
    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)
    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return mark_safe(text)