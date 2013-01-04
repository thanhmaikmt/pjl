//
//  PainterPiece.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Piece.h"
#import "DestinationPieceProtocol.h"

@class Cell;
@class TYSide;
@class TYColor;

@interface PainterPiece : Piece <DestinationPieceProtocol> 
{
	TYColor *_color;
	TYSide *_sideA;
	TYSide *_sideB;
}

@property (nonatomic, readwrite, assign) TYColor *color;
@property (nonatomic, readwrite, assign) TYSide *sideA;
@property (nonatomic, readwrite, assign) TYSide *sideB;

- (id)initWithColor:(TYColor*)color andSideA:(TYSide*)sideA andSideB:(TYSide*)sideB andCell:(Cell*)cell;

@end

@protocol PainterPieceDelegate <NSObject>

-(void)onPaint;

@end

