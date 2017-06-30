#!/bin/perl
$SIG{TERM} = \&DIE_handler
sub DIE_handler {
    print "hello";
	
}
sub hello{
	for (my $i = 1 ; $i < 9999999999;$i++){
		sleep(0.9);
		print $i;
	}
}
#main
hello();