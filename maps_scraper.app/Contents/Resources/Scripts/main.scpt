FasdUAS 1.101.10   ��   ��    l    � ����  O     �    k    �     	  I   	������
�� .miscactvnull��� ��� null��  ��   	  
  
 l  
 
��������  ��  ��        l  
 
��  ��    4 . Navigate to Google Maps Saved places directly     �   \   N a v i g a t e   t o   G o o g l e   M a p s   S a v e d   p l a c e s   d i r e c t l y      r   
     m   
    �   l h t t p s : / / w w w . g o o g l e . c o m / m a p s / c o n t r i b / y o u r - p r o f i l e / l i s t s  o      ���� 0 mapsurl mapsURL      O    ,    k    +       r    %    l   !  ����   I   !���� !
�� .corecrel****      � null��   ! �� " #
�� 
kocl " m    ��
�� 
bTab # �� $��
�� 
prdt $ K     % % �� &��
�� 
pURL & o    ���� 0 mapsurl mapsURL��  ��  ��  ��    1   ! $��
�� 
cTab   '�� ' l  & + ( ) * ( I  & +�� +��
�� .sysodelanull��� ��� nmbr + m   & '���� ��   ) + % Increased delay to ensure page loads    * � , , J   I n c r e a s e d   d e l a y   t o   e n s u r e   p a g e   l o a d s��    4    �� -
�� 
cwin - m    ����    . / . l  - -��������  ��  ��   /  0 1 0 l  - -�� 2 3��   2 + % Wait for the page to be fully loaded    3 � 4 4 J   W a i t   f o r   t h e   p a g e   t o   b e   f u l l y   l o a d e d 1  5 6 5 W   - L 7 8 7 I  B G�� 9��
�� .sysodelanull��� ��� nmbr 9 m   B C���� ��   8 =  1 A : ; : l  1 = <���� < I  1 =�� = >
�� .sfridojsnull���     ctxt = m   1 2 ? ? � @ @ & d o c u m e n t . r e a d y S t a t e > �� A��
�� 
dcnm A n   3 9 B C B 1   7 9��
�� 
cTab C 4   3 7�� D
�� 
cwin D m   5 6���� ��  ��  ��   ; m   = @ E E � F F  c o m p l e t e 6  G H G l  M M��������  ��  ��   H  I J I l  M M�� K L��   K 1 + Extract saved places data using JavaScript    L � M M V   E x t r a c t   s a v e d   p l a c e s   d a t a   u s i n g   J a v a S c r i p t J  N O N r   M _ P Q P I  M [�� R S
�� .sfridojsnull���     ctxt R m   M P T T � U U< 
                 f u n c t i o n   e x t r a c t P l a c e s ( )   { 
                         c o n s t   p l a c e s   =   [ ] ; 
                         / /   W a i t   f o r   t h e   l i s t s   t o   b e   v i s i b l e 
                         c o n s t   l i s t s   =   d o c u m e n t . q u e r y S e l e c t o r A l l ( ' . m 6 Q E r b . W N B k O b ' ) ; 
                         
                         i f   ( l i s t s . l e n g t h   = = =   0 )   { 
                                 r e t u r n   J S O N . s t r i n g i f y ( { e r r o r :   ' N o   p l a c e s   f o u n d   y e t ,   p a g e   m i g h t   s t i l l   b e   l o a d i n g ' } ) ; 
                         } 
                         
                         l i s t s . f o r E a c h ( l i s t   = >   { 
                                 c o n s t   i t e m s   =   l i s t . q u e r y S e l e c t o r A l l ( ' . b J z M E . H u 9 e 2 e . t H 5 C W c ' ) ; 
                                 i t e m s . f o r E a c h ( i t e m   = >   { 
                                         c o n s t   n a m e E l   =   i t e m . q u e r y S e l e c t o r ( ' . f o n t H e a d l i n e S m a l l ' ) ; 
                                         c o n s t   a d d r e s s E l   =   i t e m . q u e r y S e l e c t o r ( ' . f o n t B o d y M e d i u m ' ) ; 
                                         
                                         p l a c e s . p u s h ( { 
                                                 n a m e :   n a m e E l   ?   n a m e E l . t e x t C o n t e n t . t r i m ( )   :   ' U n k n o w n ' , 
                                                 a d d r e s s :   a d d r e s s E l   ?   a d d r e s s E l . t e x t C o n t e n t . t r i m ( )   :   ' U n k n o w n ' 
                                         } ) ; 
                                 } ) ; 
                         } ) ; 
                         
                         r e t u r n   J S O N . s t r i n g i f y ( p l a c e s ,   n u l l ,   2 ) ; 
                 } 
                 e x t r a c t P l a c e s ( ) ; 
         S �� V��
�� 
dcnm V n   Q W W X W 1   U W��
�� 
cTab X 4   Q U�� Y
�� 
cwin Y m   S T���� ��   Q o      ���� 0 
placesdata 
placesData O  Z [ Z l  ` `��������  ��  ��   [  \ ] \ l  ` `�� ^ _��   ^   Save the data to a file    _ � ` ` 0   S a v e   t h e   d a t a   t o   a   f i l e ]  a b a r   ` u c d c b   ` q e f e l  ` m g���� g I  ` m�� h i
�� .earsffdralis        afdr h m   ` c��
�� afdrdesk i �� j��
�� 
rtyp j m   f i��
�� 
ctxt��  ��  ��   f m   m p k k � l l , g o o g l e _ m a p s _ p l a c e s . t x t d o      ���� 0 savepath savePath b  m n m r   v � o p o I  v ��� q r
�� .rdwropenshor       file q o   v y���� 0 savepath savePath r �� s��
�� 
perm s m   | }��
�� boovtrue��   p o      ���� 0 
filehandle 
fileHandle n  t u t I  � ��� v w
�� .rdwrwritnull���     **** v o   � ����� 0 
placesdata 
placesData w �� x��
�� 
refn x o   � ����� 0 
filehandle 
fileHandle��   u  y z y I  � ��� {��
�� .rdwrclosnull���     **** { o   � ����� 0 
filehandle 
fileHandle��   z  |�� | l  � ���������  ��  ��  ��    m      } }�                                                                                  sfri  alis    p  Preboot                    ����BD ����
Safari.app                                                     �����l�        ����  
 cu             Applications  F/:System:Volumes:Preboot:Cryptexes:App:System:Applications:Safari.app/   
 S a f a r i . a p p    P r e b o o t  -/Cryptexes/App/System/Applications/Safari.app   /System/Volumes/Preboot ��  ��  ��       �� ~ ��   ~ ��
�� .aevtoappnull  �   � ****  �� ����� � ���
�� .aevtoappnull  �   � **** � k     � � �  ����  ��  ��   �   �   }�� ���������������������� ?���� E T���������� k��������������
�� .miscactvnull��� ��� null�� 0 mapsurl mapsURL
�� 
cwin
�� 
kocl
�� 
bTab
�� 
prdt
�� 
pURL�� 
�� .corecrel****      � null
�� 
cTab�� 
�� .sysodelanull��� ��� nmbr
�� 
dcnm
�� .sfridojsnull���     ctxt�� 0 
placesdata 
placesData
�� afdrdesk
�� 
rtyp
�� 
ctxt
�� .earsffdralis        afdr�� 0 savepath savePath
�� 
perm
�� .rdwropenshor       file�� 0 
filehandle 
fileHandle
�� 
refn
�� .rdwrwritnull���     ****
�� .rdwrclosnull���     ****�� �� �*j O�E�O*�k/ *�����l� 
*�,FO�j UO h��*�k/�,l a  kj [OY��Oa �*�k/�,l E` Oa a a l a %E` O_ a el E` O_ a _ l O_ j OPU ascr  ��ޭ