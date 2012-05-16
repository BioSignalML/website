######################################################
#
#  BioSignalML Management in Python
#
#  Copyright (c) 2010  David Brooks
#
#  $Id$
#
######################################################

"""A web.py application powered by Tornado"""

import os
import logging

import tornado.httpserver
import tornado.web
from tornado.options import options, define


class Ontologies(tornado.web.RequestHandler):
#============================================

  def get(self, name):
  #-------------------
    # Check accept header and send RDF...
    self.write(name)
    #self.render('ontologies.html')


class WebPages(tornado.web.RequestHandler):
#==========================================

  def get(self, name=None):
  #------------------------
    self.redirect('http://code.google.com/p/biosignalml/')
    #render('webpage.html', title='Testing...')


if __name__ == '__main__':
#=========================

  define('debug', True)
  define('host', 'localhost')
  define('port', 8085)

  static_path = os.path.join(os.path.dirname(__file__), 'static')
  ontology_path = os.path.join(os.path.dirname(__file__), 'ontologies/2011/04')

  application = tornado.web.Application([
      (r'/ontologies/2011.04/(.*)', tornado.web.StaticFileHandler, {'path': ontology_path }),
      (r'/ontologies/(.*)',                 Ontologies),
      (r'/static/(.*)',             tornado.web.StaticFileHandler, {'path': static_path }),
      (r'/(.*)',                            WebPages),
      (r'',                                 WebPages),      
      ],
    gzip = True,
    template_path = 'templates',
    debug = options.debug,
    )

  application.listen(options.port, options.host, xheaders=True)
  logging.info('Starting http://%s:%d/', options.host, options.port)

  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    pass