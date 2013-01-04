//
//  Yard.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "Yard.h"
#import "Cell.h"
#import "ModelChangeEvent.h"
#import "Piece.h"
#import "PieceType.h"
#import "EmptyPiece.h"
#import "TrackPiece.h"
#import "TYTrack.h"

@implementation Yard

@synthesize cols = _cols;
@synthesize rows = _rows;

+(id) yardWithCols: (int) cols andRows: (int) rows andCells: (NSMutableArray*) cells
{
	return [[[Yard alloc] initWithCols:cols andRows:rows andCells:cells] autorelease];
}

-(id) initWithCols: (int) cols andRows: (int) rows andCells: (NSMutableArray*) cells
{
	self = [super init];
	if(self)
	{
		_cols = cols;
		_rows = rows;
		_cells = [cells retain];
		
		for(Cell *cell in _cells)
		{
			cell.delegate = self;
		}
	}
	return self;
}

-(tyPieceCounts) getPieceCounts
{
    tyPieceCounts pieceCounts = {0,0,0,0,0,0};
    
    for (Cell *cell in _cells)
    {
        if(cell.piece.pieceType == PieceType_Empty) pieceCounts.empty++;
        else if(cell.piece.pieceType == PieceType_Outlet) pieceCounts.outlet++; 
        else if(cell.piece.pieceType == PieceType_Goal) pieceCounts.goal++; 
        else if(cell.piece.pieceType == PieceType_Rock) pieceCounts.rock++; 
        else if(cell.piece.pieceType == PieceType_Painter) pieceCounts.painter++; 
        else if(cell.piece.pieceType == PieceType_Splitter) pieceCounts.splitter++;         
    }
    
    return pieceCounts;
}

-(Cell*) getCellNextToCell:(Cell*)currentCell onSide:(TYSide*)side
{
	Cell *nextCell = nil;
	
	int col = NSNotFound;
	int row = NSNotFound;
	
	switch(side.value)
	{
		case TYSide_Top:
			col = currentCell.col;
			row = currentCell.row-1;
			break;
		case TYSide_Right:
			col = currentCell.col+1;
			row = currentCell.row;
			break;
		case TYSide_Bottom:
			col = currentCell.col;
			row = currentCell.row+1;
			break;
		case TYSide_Left:
			col = currentCell.col-1;
			row = currentCell.row;
			break;			
	}
	
	if(col!=NSNotFound && row!=NSNotFound && col >= 0 && col <_cols && row >= 0 && row < _rows)
	{
		nextCell = [_cells objectAtIndex:(row*_cols)+col];
	}
	
	return nextCell;
}

-(Cell*) getCellByCol:(int)col andRow:(int)row
{
	return [_cells objectAtIndex:row*_cols + col];
}

-(void) removeTracksAndFireChange:(BOOL)shouldFireChange
{
	for(Cell *cell in _cells)
	{
		if(cell.piece.pieceType == PieceType_Track)
		{
			cell.piece.cell = nil;
			cell.piece = [[[EmptyPiece alloc] initWithCell:cell] autorelease];
		}
	}
	
	if(shouldFireChange) [self fireMinorChange];
}

-(int) getTrackCount
{
	int trackCount = 0;
	for(Cell *cell in _cells)
	{	
		//A track piece counts for 1000, having two tracks counts for 1 more point... Lower is better
		
		if(cell.piece.pieceType == PieceType_Track)
		{
			trackCount+=1000;
			
			if(((TrackPiece*)cell.piece).secondaryTrack.value != TYTrack_Empty)
			{
				trackCount+=1; 
			}
		}
	}
		
	return trackCount;
}

-(Cell*) getCellAtIndex: (int) index
{
	return [_cells objectAtIndex:index];
}

-(void) update:(float)deltaTime
{
	if([(id<YardDelegate>)_delegate respondsToSelector:@selector(onUpdate:)])
	{
		[(id<YardDelegate>)_delegate onUpdate:deltaTime];
	}
	
	if([(id<YardDelegate>)_viewDelegate respondsToSelector:@selector(onUpdate:)])
	{
		[(id<YardDelegate>)_viewDelegate onUpdate:deltaTime];
	}
}

//Convenience method to make things FASTER
-(NSArray*)getCells
{
	return _cells;
}

//BUBBLE THE EVENTS UP FROM THE CELLS
-(void) onMajorChange: (ModelChangeEvent*)event
{
	[self fireMinorChangeWithThingThatChanged:event.thingThatChanged];
}

-(void) onMinorChange: (ModelChangeEvent*)event
{
	[self fireMinorChangeWithThingThatChanged:event.thingThatChanged];
}


- (id)copyWithZone:(NSZone *)zone
{
	NSMutableArray *newCells = [NSMutableArray array];

	for(Cell *cell in _cells)
	{
		[newCells addObject:[[cell copyWithZone:zone] autorelease]]; //deep copy
	}
	
	return  [[[self class] alloc] initWithCols:_cols andRows:_rows andCells:newCells];
}
 

-(void) dealloc
{
	//NSLog(@"yard go boom");
	[_cells release];
	[super dealloc];
}

-(NSString*) description
{
	NSMutableString *result = [NSMutableString stringWithFormat:@"\n[Yard %d,%d: \n", _cols, _rows];
	for(Cell *cell in _cells)
	{
		[result appendString:[NSString stringWithFormat:@"\t%@\n", cell]];
	}
	[result appendString:@"]"];
	return result;
}


@end
