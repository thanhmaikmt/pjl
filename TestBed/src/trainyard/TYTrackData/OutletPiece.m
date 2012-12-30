//
//  OutletPiece.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "OutletPiece.h"
#import "Cell.h"
#import "TYColor.h"
#import "TYSide.h"
#import "PieceDecoder.h"
#import "YardStringEncoder.h"
#import "Train.h"

@implementation OutletPiece

@synthesize colors = _colors;
@synthesize sideOut = _sideOut;

- (id)initWithColors:(NSMutableArray*)colors andSideOut:(TYSide*)sideOut andCell:(Cell*)cell;
{
	self = [super initWithPieceType:PieceType_Outlet andCell:cell];
	if(self)
	{
		_colors = [colors retain];
		_sideOut = sideOut;
	}
	return self;
}

-(BOOL) hasTrains
{
	return ([_colors count] > 0);
}

-(NSArray*) getTrainsToCreate
{
	if([_colors count] > 0) //returns one train at a time
	{
		NSArray *result = [NSArray arrayWithObject:[[[Train alloc] initWithColor:[_colors objectAtIndex:0] 
																		andPiece:self 
																	 andNextSide:_sideOut] autorelease]];
		[_colors removeObjectAtIndex:0];
		
		//tell the delegates that the train has been sent
		if([_delegate respondsToSelector:@selector(onSendTrain:)])
		{
			[(id)_delegate onSendTrain:0];
		} 
		
		if([_viewDelegate respondsToSelector:@selector(onSendTrain:)])
		{
			[(id)_viewDelegate onSendTrain:0];
		}
		
		[self fireMinorChange]; //a major change would have made the view create all new nubs
		
		return result;
	}
	else
	{
		return [NSArray array]; //empty array
	}
}

-(void) toEncodedChars: (char[]) chars
{
	chars[0] = 'O';
	
	chars[1] = charFromInt(_sideOut.value*9 + [_colors count]-1);
	
	int charIndex = 2;

	for(int c = 0; c<[_colors count]; c++)
	{	
		TYColor *color = [_colors objectAtIndex:c];
		int colorValue = color.value*7;
		
		c++;
		
		if(c < [_colors count])
		{
			color = [_colors objectAtIndex:c];
			colorValue += color.value;
		}
				
		chars[charIndex++] = charFromInt(colorValue);
	}
	
	chars[charIndex] = '\0';
}


+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars
{
	int firstCharValue = intFromChar(chars[1]);
	TYSide *sideOut = [TYSide sideFromValue:floor((float)firstCharValue/9)];
	int numColors = (firstCharValue%9)+1;
	
	NSMutableArray *colors = [NSMutableArray array];
	
	int c = 0;
	
	//two colors are packed into every char
	while ([colors count] < numColors) 
	{
		int charValue = intFromChar(chars[c+2]);
		[colors addObject:[TYColor colorFromValue:floor((float)charValue/7)]];
		
		if([colors count] < numColors) 
		{
			[colors addObject:[TYColor colorFromValue:charValue%7]];
		}
		
		c++;
	}
	
	OutletPiece *piece = [[[OutletPiece alloc] initWithColors:colors andSideOut:sideOut andCell:nil] autorelease];
	return [PieceDecoder pieceDecoderWithPiece:piece andNumCharsToRemove:c+2];
}

- (id)copyWithZone:(NSZone *)zone
{
	return  [[[self class] alloc] initWithColors:[[_colors mutableCopyWithZone:zone] autorelease] andSideOut:_sideOut andCell:_cell];
}

-(NSString*) description
{
	char colorChars[[_colors count]];
	
	int c = 0;
	for(TYColor *color in _colors)
	{
		colorChars[c++] = color.shortForm;
	}
	colorChars[c] = '\0';
	
	return [NSString stringWithFormat:@"{Piece %@ SideOut:%@ Colors:%s}", NSStringFromPieceType(_pieceType), _sideOut, colorChars];
}

-(void) dealloc
{
	[_colors release];
	
	[super dealloc];
}


@end
