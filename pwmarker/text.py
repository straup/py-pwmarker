import cairo
import re

class text :

    def __init__ (self) :

        self.surface = None

        self.font_face_header = "Helvetica Bold"
        self.font_size_header = 18
        
        self.font_face_body = "Helvetica Bold"
        self.font_size_body = 11

        self.width = 0
        self.height = 0
        
        self.max_width = 0
        
        self.margin = 20
        self.ln_height_body = 0

    #
    
    def draw (self, header, body) :

        (header, body) = self.calculate(header, body)
        
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(self.surface)

        # basic setup
        
        ctx.move_to(0, 0)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.set_source_rgb(255, 255, 255)
        ctx.fill()

        ctx.set_source_rgb(0, 0, 0)

        # first the header
        
        x = 0 + self.margin
        y = 0 + (self.margin * 2)
        ctx.move_to(x, y)

        ctx.select_font_face(self.font_face_header, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)    
        ctx.set_font_size(self.font_size_header)

        for part in header :
            ctx.show_text(part)
            y = y + int(self.margin * 1.5)
            ctx.move_to(x, y)

        # now the body
        
        ctx.select_font_face(self.font_face_body, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)    
        ctx.set_font_size(self.font_size_body)

        # fix me : allow for multiple paragraphs
        
        for txt in body :
            ctx.show_text(txt)
            y = y + self.ln_height_body
            ctx.move_to(x, y)       

    #
    
    def calculate (self, header, body) :

        chunks_header = []
        chunks_body = []
        
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(self.surface)

        # fix me : chunkify the header
        
        ctx.select_font_face(self.font_face_header, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(self.font_size_header)

        (tw, th) = self.measure_text(ctx, header)

        if tw > (self.width - (self.margin * 2)) :
            self.width = tw + (self.margin * 2)

        chunks_header = self.chunkify(ctx, header)

        #
        
        ctx.select_font_face(self.font_face_body, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)    
        ctx.set_font_size(self.font_size_body)

        chunks_body = self.chunkify(ctx, paras)

        # sort out line height

        self.ln_height_body = int(max(map(lambda word: word[1], map(lambda ln: self.measure_text(ctx, ln), chunks_body))) * 1.5)

        #
        
        self.height += int(self.margin * (3 + len(chunks_body)))

        self.width = int(self.width)
        self.height = int(self.height)

        return (chunks_header, chunks_body)

    #

    def chunkify_header(self, ctx, header) :
        return self.chunkify(ctx, header)

    #
    
    def chunkify_body (self, ctx, paras) :

        chunks = []

        for txt in paras :
            chunks.extend(self.chunkify(ctx, txt))

        return chunks

    #
    
    def chunkify (self, ctx, txt) :

        chunks = []
        chunk = txt

        okw = self.width - (self.margin * 2)
    
        while len(chunk) :
            (dw, dh) = self.measure_text(ctx, chunk)

            self.height += dh
        
            if dw < okw :
                chunks.append(chunk)
                break

            foo = ''
        
            for i in range(0, int(dw)) :
                foo += chunk[i]

                (fw, fh) = self.measure_text(ctx, foo)

                if fw < okw :
                    continue
                else :
                    stuff = foo[:-1]

                match = re.findall("(\s([^\s]+))$", stuff)

                if len(match) :
                    rest = match[0][0]
                    l = len(rest)
                    stuff = stuff[:-l]
                    
                    chunks.append(stuff)
                    chunk = rest.strip() + chunk[i:]
                    
                    break

        return chunks
        
    #
    
    def save (self, path) :
        self.surface.write_to_png(path)

    #

    def measure_text (self, ctx, txt):
            
        xbearing, ybearing, width, height, xadvance, yadvance = (
            ctx.text_extents(unicode(txt)))
        
        return (width, height)

    #
    
if __name__ == '__main__' :

    title = "this is the header"
    paras = ["this is the body. it is very long, and has many run on sentences"]

    t = text()
    t.draw(title, paras)

    t.save("/home/asc/Desktop/t.png")
