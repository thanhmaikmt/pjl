//
//  Yard.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Model.h"
#import "TYSide.h"

@class Cell;

typedef struct _tyPieceCounts
{
    int empty;
    int outlet;
    int goal;
    int rock;
    int splitter;
    int painter;    
} tyPieceCounts;

@interface Yard : Model <ModelDelegate>
{
	int _cols;
	int _rows;
	NSMutableArray *_cells;
}

@property (nonatomic, readonly) int cols;
@property (nonatomic, readonly) int rows;

+(id) yardWithCols: (int) cols andRows: (int) rows andCells: (NSMutableArray*) cells;
-(id) initWithCols: (int) cols andRows: (int) rows andCells: (NSMutableArray*) cells;

-(tyPieceCounts) getPieceCounts;

-(Cell*) getCellNextToCell:(Cell*)currentCell onSide:(TYSide*)side;
-(Cell*) getCellByCol:(int)col andRow:(int)row;
-(void) removeTracksAndFireChange:(BOOL)shouldFireChange;
-(int) getTrackCount;

-(Cell*) getCellAtIndex: (int) index;

-(void) update: (float) deltaTime;

-(NSArray*)getCells; //convenience

@end

@protocol YardDelegate <NSObject>

-(void) onUpdate:(float)deltaTime;

@end

