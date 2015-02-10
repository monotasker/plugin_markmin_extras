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

# FIXME: need better way of normalizing db calls across apps
imgtbls = ['blog_images', 'woh_images', 'paideia_images', 'images']
imgtable = [db[t] for t in imgtbls if t in db.tables][0]
imgrows = db(imgtable['id'] > 0).select().as_list()

audtbls = ['woh_audio', 'paideia_audio', 'audio']
audtable = [db[t] for t in audtbls if t in db.tables][0]
audrows = db(audtable['id'] > 0).select().as_list()


def maketag(tbl, ttf, flf, txt):
    """docstring for maketag"""
    tbl = tbl if isinstance(tbl, list) else [tbl]
    mytbl = [db[t] for t in tbl if t in db.tables]
    if not mytbl:
        return False
    url = URL('plugin_markmin_extras', 'download',
              mytbl(mytbl[ttf] == txt)[mytbl[flf]]
              ).xml()
    return url

# any variable names in this dict can be called in markmin code using
# the ``mytext``:varname syntax.
mm_extras = dict(img_by_title=lambda text: maketag(['blog_images', 'woh_images',
                                                    'paideia_images', 'images'],
                                                   'image_title',
                                                   'img_file', text),
                 audio_by_title=lambda text: maketag(['woh_audio', 'paideia_audio',
                                                      'audio'],
                                                     'audio_title',
                                                     'audio_file_mp3', text),
                 doc_by_title=lambda text: maketag(['docs'], 'label',
                                                   'docfile', text),
                 youtube=lambda text: '<iframe width="560" height="315" '
                     'style="margin:0 auto; display:block;" '
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
