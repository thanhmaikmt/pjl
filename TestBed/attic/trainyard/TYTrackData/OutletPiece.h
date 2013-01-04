//
//  OutletPiece.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Piece.h"
#import "CreatorPieceProtocol.h"
#import "Model.h"

@class Cell;
@class TYSide;

@interface OutletPiece : Piece <CreatorPieceProtocol>
{
	NSMutableArray *_colors;
	TYSide *_sideOut;
}

@property (nonatomic, readwrite, retain) NSMutableArray *colors;
@property (nonatomic, readwrite, assign) TYSide *sideOut;

- (id)initWithColors:(NSMutableArray*)colors andSideOut:(TYSide*)sideOut andCell:(Cell*)cell;

@end

@protocol OutletPieceDelegate <NSObject>

-(void)onSendTrain:(int)trainIndex;

@end

