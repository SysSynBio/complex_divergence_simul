rm(list = ls())
require(ggplot2)
require(grid)
require(latticeExtra)

last.letter <- function(this.string) {tmp.length <- nchar(this.string); substring(this.string, tmp.length, tmp.length)}

mycols <- dput(ggplot2like(n = 5, h.start = 0, l = 65)$superpose.line$col)

cbbPalette <- c('WT' = "#000000", 'UnB' = mycols[1], 'UnS' = mycols[2])

interface.plot <- function(df) {
  graphics.off()
  the_pointsize=18
  theme_set(theme_bw(base_size=the_pointsize))
  old_theme <- theme_update(panel.border=element_blank(),
                            axis.line=element_line(),
                            panel.grid.minor=element_blank(),
                            panel.grid.major=element_blank(),
                            panel.background=element_blank(),
                            panel.border=element_blank(),
                            axis.line=element_line())
  
  g <- ggplot(df, aes(x=int.frac, fill=id, color=id)) + 
    geom_density(alpha=0.2) + 
    scale_colour_manual(values=cbbPalette) + 
    scale_fill_manual(values=cbbPalette)
  g <- g + theme(strip.background=element_blank())
  g <- g + ylab('Probability Density')
  g <- g + xlab('Odds of accepting Non-interface to Interface Mutations')
  g <- g + scale_x_continuous(breaks=seq(0, 6, 1), limits=c(0, 6))
  g <- g + theme(panel.border=element_blank(), axis.line=element_line())
  g <- g + theme(axis.title.x = element_text(size=24, vjust=-1))
  g <- g + theme(axis.text.x = element_text(size=24))
  g <- g + theme(axis.title.y = element_text(size=24, vjust=2))
  g <- g + theme(axis.text.y = element_text(size=24))
  g <- g + theme(axis.line = element_line(colour = 'black', size = 1))
  g <- g + theme(axis.ticks = element_line(colour = 'black', size = 1))
  g <- g + theme(plot.margin=unit(c(1.5, 1.5, 1.5, 1.5), "lines"))
  g <- g + theme(axis.ticks.margin = unit(0.25, "cm"))
  g <- g + theme(legend.position = c(0.75, 0.9),
                 legend.title=element_blank(), 
                 legend.key = element_blank(), 
                 legend.text=element_text(size=22),
                 legend.key.size = unit(1, "cm"))
  
  ggsave(g, file=paste('~/Desktop/interfacial.pdf', sep=''), width=12, height=10)
  return(g)
}

WT <- read.table('~/Desktop/WT_Interface.txt', header=T)
UnB <- read.table('~/Desktop/UnB_Interface.txt', header=T)
UnS <- read.table('~/Desktop/UnS_Interface.txt', header=T)

plot.data <- data.frame(id=c(rep('WT', length(WT$interface)), rep('UnB', length(UnB$interface)), rep('UnS', length(UnS$interface))), 
                        int.frac=c(WT$non_interface/WT$interface, UnB$non_interface/UnB$interface, UnS$non_interface/UnS$interface))

interface.plot(plot.data)