# THIS IS NOT CONSIDERED STABLE YET.

import re
import cairo

#
# Private...don't come crying to me
#

def _pil2cairo (img) :

        # check me...
        img = img.convert('RGBA')
        
        (w, h) = img.size

	mode = cairo.FORMAT_ARGB32

        data = img.tostring()
        a = array.array('B', data)

        return cairo.ImageSurface.create_for_data (a, mode, w, h, (w * 4))

def _cairo2pil(surface) :

	mode='RGBA'
        
        width = surface.get_width()
        height = surface.get_height()
    
        return PIL.Image.frombuffer(mode, (width, height), surface.get_data(), "raw", mode, 0, 1)

def _assign_font_details (ctx, **kwargs) :
        
        font_face = "Helvetica"
        font_size = 12;

        if kwargs.has_key('font_face') :
                font_face = kwargs['font_face']

        if kwargs.has_key('font_size') :
                font_size = kwargs['font_size']

        ctx.select_font_face(font_face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)

def _measure_text (ctx, txt):

        xbearing, ybearing, width, height, xadvance, yadvance = (ctx.text_extents(unicode(txt)))

        # honestly, I have no idea why I need to do this
        # but it seems necessary for long pieces of text
        # ...
        
        if width == 0.0 or width < len(txt) :
                ext = ctx.text_extents(unicode(txt))
                width = ext[2]
                height = ext[3]

        return (width, height)

def _offsets_for_page_number(ctx, pg_number) :

        # http://www.tortall.net/mu/wiki/CairoTutorial#tips-and-tricks
        
        fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
        
        xbearing, ybearing, width, height, xadvance, yadvance = (
            ctx.text_extents(unicode(pg_number)))
        
        x = 0.5 - xbearing - width / 2
        y = fdescent + fheight / 2

        # wtf do I need to adjust these again by hand?
        
        x = x - 1                
        y = y - int(height * 1.5)

        if int(pg_number) >= 10 :
                x = x - 2
                
    	return (x, y)

#
# Public
# 

def draw_text_block_to_PIL (text, width, height, **kwargs) :
        cairo_surface = draw_text_block(text, width, height, **kwargs)
        return _cairo2pil(cairo_surface)

# ##########################################################

def draw_text_block_to_PNG (text, path, width, height, **kwargs) :
        cairo_surface = draw_text_block(text, width, height, **kwargs)
        cairo_surface.write_to_png(path)
        
# ##########################################################

def draw_text_block (text, width, height, **kwargs) :

        surface = None
        ctx = None
        
        if kwargs.has_key('cairo_surface') :
                surface = kwargs['cairo_surface']
                ctx = cairo.Context(surface)

        else :
                surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)                
                ctx = cairo.Context(surface)

        #

        _assign_font_details(ctx, **kwargs)
        
        #
        
        if kwargs.has_key('ensure_width') :
                (w, h) = _measure_text(ctx, text)

                if w > width :
                        width = int(w * 1.25)
                        
        #
                        
        chunks = []

        ok_width = width
        ok_height = height
        
        margin_x = 0
        margin_y = 0

        padding_x = 0
        padding_y = 0

        if kwargs.has_key('margin') and int(kwargs['margin']) > 0:
                ok_width -= (kwargs['margin'] * 2)
                ok_height -= (kwargs['margin'] * 2)
                
                margin_x += kwargs['margin']
                margin_y += kwargs['margin']
                                
        if kwargs.has_key('padding_left') and int(kwargs['padding_left']) > 0:
                ok_width -= kwargs['padding_left']
                margin_x = kwargs['padding_left']

        if kwargs.has_key('padding_right') and int(kwargs['padding_right']) > 0:
                ok_width -= kwargs['padding_right']

        if kwargs.has_key('padding_top') and int(kwargs['padding_top']) > 0:
                ok_height -= kwargs['padding_top']
                margin_y = kwargs['padding_top']

        if kwargs.has_key('padding_bottom') and int(kwargs['padding_bottom']) > 0:
                ok_height -= kwargs['padding_bottom']
        
        # hack, clean up variable names...
        desc = text

        ln_height = 0

        while len(desc) :
                
                (desc_width, desc_height) = _measure_text(ctx, desc)

                height += desc_height

                ln_height = max(ln_height, desc_height)
                        
                if desc_width < ok_width :
                        chunks.append(desc)
                        break

                buffer = ''

                for i in range(0, len(desc)) :
                        
                        buffer += desc[i]
                        
                        (fw, fh) = _measure_text(ctx, buffer)

                        ln_height = max(ln_height, fh)
                        
                        if fw < ok_width :
                                continue
                        else :

                                snippet = buffer[:-1]

                                match = re.findall("(\s([^\s]+))$", snippet)

                                if len(match) :
                                        rest = match[0][0]
                                        l = len(rest)
                                        snippet = snippet[:-l]
                    
                                        chunks.append(snippet)
                                        desc = rest.strip() + desc[i:]
                
                                        break

        width = int(width)
        height = int(height)
    
        # surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        # ctx = cairo.Context(surface)

        if not kwargs.has_key('no_background') :
                ctx.move_to(0, 0)
                ctx.rectangle(0, 0, width, height)
                ctx.set_source_rgb(255, 255, 255)
                ctx.fill()
        
        ctx.set_source_rgb(0, 0, 0)
    
        x = margin_x + padding_x
        y = margin_y + padding_y + ln_height
                        
        ctx.move_to(x, y)

        # hrmmm....
        ln_height = 20
        
        for txt in chunks :

                txt = txt.strip()
                ok = 1
                
                for ln in txt.split("\n") :

                        if ln.strip() != '' :
                                ctx.show_text(ln)
                                
                        y = y + int(ln_height)

                        if y > ok_height :
                                ok = 0
                                break
                        else :
                                ctx.move_to(x, y)       
                if not ok :
                        break
                
        return surface


# ##########################################################

def draw_circle_with_string (surface, args) :

        bg_c = (255, 255, 255)
        str_c = (0, 0, 0)
        txt_c = (0, 0, 0)
        
        if args.has_key('background_c'):
                bg_c = args['background_c']

        if args.has_key('stroke_c'):
                str_c = args['stroke_c']

        if args.has_key('text_c'):
                txt_c = args['text_c']

        x = args['x']
        y = args['y']
        r = args['radius']
        a = 0

        if args.has_key('anchor_height') :
                a  = args['anchor_height']

        if a != 0 :
                y = y - (a + int(args['radius'] / 2))
        
        if a != 0 :
                ctx = cairo.Context(surface)        
                ctx.move_to(args['x'], args['y'])
                ctx.set_source_rgb(str_c[0], str_c[1], str_c[2])            
                ctx.set_line_width(2)
                ctx.line_to(args['x'], (args['y'] - a))
                ctx.stroke()

        ctx = cairo.Context(surface)        
        ctx.move_to(x, y)
        ctx.arc(x, y, r, 0, 360)
        ctx.set_source_rgb(bg_c[0], bg_c[1], bg_c[2])
        ctx.fill()
        
        ctx = cairo.Context(surface)
        ctx.arc(x, y, r, 0, 360)        
        ctx.set_source_rgb(str_c[0], str_c[1], str_c[2])
        ctx.set_line_width(2)
        ctx.stroke()
    
        ctx = cairo.Context(surface)                                
        ctx.set_source_rgb(txt_c[0], txt_c[1], txt_c[2])    
    
        offset_x, offset_y = _offsets_for_page_number(ctx, args['string'])
    
        x = x + offset_x
        y = y - offset_y

        _assign_font_details(ctx, font_face='Helvetica Bold')
        
        ctx.move_to(x, y)
        ctx.show_text(unicode(args['string']))
