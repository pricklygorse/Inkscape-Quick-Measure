#!/usr/bin/env python
# coding=utf-8
# inkscape 1.2

import inkex

from inkex.bezier import csplength


class MeasureLength(inkex.EffectExtension):
   
    
    def add_arguments(self, pars):
       pars.add_argument(
            "-u", "--unit", default="px", help="The unit of the measurement"
        )

    def effect(self):
       
        
        try:
                 if float(inkex.__version__[:3]) >= 1.2:
                   viewport_code = True
                   
                 else:
                   viewport_code = False
                  
        except Exception:
                 
                 viewport_code = False
        
        
        
        
        # Calculate the unit factor depending on the inkscape version
        # unittouu is not officially depreciated but is not recommended
        # The output of unittouu has changed in the past.
        
        if viewport_code == False:
        
          #############################
          # inkscape 1.1 code block
          prec = 2
          scale = self.svg.unittouu('1px')  # convert to document units
          factor = 1.0

          if self.svg.get('viewBox'):
            factor = self.svg.scale / self.svg.unittouu('1px')

          factor *= scale / self.svg.unittouu('1' + self.options.unit)
          
        
        else:
          
          #inkscape 1.2 and newer
          prec = 2
          scale = self.svg.viewport_to_unit(
            "1" + self.svg.document_unit
          )  # convert to document units
          factor = self.svg.unit_to_viewport(1, self.options.unit)
        


        # loop over all selected paths
        filtered = self.svg.selection.filter(inkex.PathElement)
        
        
        if not filtered:
            raise inkex.AbortExtension(_("Please select at least one path object."))
        
        for node in filtered:
            
            csp = node.path.transform(node.composed_transform()).to_superpath()
                        
            slengths, stotal = csplength(csp)
            
            # convert segment lengths into user defined units.
            slengths_uu = []
            cumulative = [0]
            count = 0
            for number in slengths[0]:
                 length_user_unit = round(number * factor, prec)
  
                 slengths_uu.append(length_user_unit)
                 
                 count += number
                 
                 cumulative.append(round(count * factor,prec))
        
            self.msg("Total length: " + str(round(stotal * factor,2))+" "+self.options.unit)
            self.msg("Segment Lengths: " + str(slengths_uu)+" "+self.options.unit)
            self.msg("Cumulative Lengths: " + str(cumulative)+" "+self.options.unit)
            self.msg("")

           
if __name__ == "__main__":
    MeasureLength().run()
