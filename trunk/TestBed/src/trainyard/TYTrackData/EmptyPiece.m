//
//  EmptyPiece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "EmptyPiece.h"
#import "Cell.h"
#import "PieceDecoder.h"

@implementation EmptyPiece

- (id)initWithCell: (Cell*) cell
{
	self = [super initWithPieceType:PieceType_Empty andCell:cell];
	return self;
}

+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars
{
	EmptyPiece *piece = [[[EmptyPiece alloc] initWithCell:nil] autorelease];
	return [PieceDecoder pieceDecoderWithPiece:piece andNumCharsToRemove:1];
}

-(void) undo
{
	if([_delegate respondsToSelector:@selector(onUndo)])
	{
		[(id)_delegate onUndo];
	}
	if([_viewDelegate respondsToSelector:@selector(onUndo)])
	{
		[(id)_viewDelegate onUndo];
	}  
}

- (id)copyWithZone:(NSZone *)zone
{
	return  [[EmptyPiece alloc] initWithCell:_cell];
}



@end
