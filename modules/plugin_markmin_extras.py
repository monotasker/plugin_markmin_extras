#! /usr/bin/python
# -*- coding:utf8 -*-

"""
plugin_markmin_extras

A collection of standard extensions to web2py's markmin markup system.

The following extensions will include html tags for an image, a playable audio
file, or a generic uploaded document. Rather than having to know the full
filename (which web2py obscures for uploaded files), the file can be identified
by its assigned title in the database table which handles that upload type.

``mygreattitle``:image_by_title
``mygreattitle``:audio_by_title
``mygreattitle``:doc_by_title

To access these markmin extensions, include the "extra" parameter when you
invoke the MARKMIN() helper, like this:

    MARKMIN(slide.slide_content, extra=mm_extras)

This plugin assumes the accompanying controller function (also in the
packaged plugin) to provide download access to the files.

"""
# from pprint import pprint
from gluon import current, URL
db = current.db


# user configured table and field sources
tag_types = {'image': ['blog_images', 'image_title', 'img_file'],
             'audio': ['woh_audio', 'audio_title', 'audio_file_mp3', 'audio_file_ogg'],
             'upload': ['docs', 'label', 'docfile']
             }

td = {tag_type: {'table': db[data[0]],
                 'titlefield': db[data[0]][data[1]],
                 'filefield': db[data[0]][data[2]]}
      for tag_type, data in tag_types.iteritems()}

imgrows = db(db.blog_images.id > 0).select().as_list()
imgrows2 = db(db.woh_images.id > 0).select().as_list()
audrows = db(db.woh_audio.id > 0).select().as_list()
docrows = db(db.docs.id > 0).select().as_list()


def maketag(td, t, txt):
    """docstring for ma"""
    url = URL('plugin_markmin_extras', 'download',
              td[t]['table'](td[t]['titlefield'] == txt)[td[t]['filefield']]
              ).xml()
    return url

# any variable names in this dict can be called in markmin code using
# the ``mytext``:varname syntax.
mm_extras = dict(img_by_title=lambda text: maketag(td, 'image', text),
                 audio_by_title=lambda text: maketag(td, 'audio', text),
                 doc_by_title=lambda text: '<a href={}>{}</a> '
                     ''.format(URL('blog/plugin_markmin_extras', 'download',
                                   [d['docfile'] for d in docrows
                                   if d['label'] == text][0]
                                   ),
                               text),
                 youtube=lambda text: '<iframe width="560" height="315" '
                     'src="https://www.youtube.com/embed/{}" frameborder="0" '
                     'allowfullscreen></iframe>'.format(text),
                 img=lambda text: '<img class="center" src="{}" '
                     '/>'.format(URL('static/images', [i for i in imgrows
                                     if i['title'] == text][0]['image'])),
                 img_r=lambda text: '<img class="pull-right" src="{}" '
                     '/>'.format(URL('static/images', [i for i in imgrows
                                     if i['title'] == text][0]['image'])),
                 img_l=lambda text: '<img src="{}" class="pull-left" '
                     '/>'.format(URL('static/images', [i for i in imgrows
                                     if i['title'] == text][0]['image'])),
                 audio=lambda text: [i for i in audrows
                                     if i['title'] == text][0]['audio']
                 )
