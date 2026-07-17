# esense og Midnight: byggeavgjørelse

## Beslutning

esense skal først være et godt dokumentasjonsverktøy. Midnight er et valgfritt
integritetslag som kan bevise at en bestemt, beskyttet dokumentversjon eksisterte
og ikke senere ble endret. Midnight skal ikke være dokumentlager, brukerregister,
tilgangssystem eller juridisk beslutningsmotor.

## Det som allerede er bygget

- Den godkjente planversjonen fryses sammen med utført arbeid, prøving, avvik og
  overleveringsinformasjon.
- Det private innholdet krypteres i esense med AES-256-GCM.
- En tilfeldig saltet SHA-256-forpliktelse og en lokal serverkvittering opprettes.
- Eier, senere utførende virksomhet og myndighet kan få uttrykkelig tilgang med
  formål. Tidsavgrenset tilgang kan trekkes tilbake.
- Grensesnittet viser `Ikke forankret` helt til en ekte transaksjon er bekreftet.

## Det som aldri skal på blokkjeden

- navn, e-post, adresse eller personidentifikator;
- oppdragsnummer, kundenummer eller intern anleggsreferanse;
- rapporttekst, målinger, bilder, filnavn eller avvik;
- organisasjonsmedlemskap, rolle eller tilgangsformål.

Kun en 32-byte forpliktelse til en saltet dokumentversjon kan registreres.

## Første Preprod-pilot

1. Prøv hele esense-flyten med minst tre representative skoleoppdrag.
2. La lærer, elev og en tenkt dokumentmottaker kontrollere at rapportvisningen er
   forståelig og at tilbakekalling virker.
3. Opprett en separat testlommebok uten produksjonsmidler.
4. Kjør den offisielle, versjonsfestede proof server lokalt på Cardano-serveren,
   kun tilgjengelig fra DApp-tjenesten på port 6300.
5. Kompiler og test kvitteringskontrakten separat fra esense.
6. Registrer én syntetisk forpliktelse på Preprod og lagre nettverk,
   kontraktadresse, transaksjons-ID og bekreftelsestid i en egen ankertabell.
7. Kontroller transaksjonen gjennom en uavhengig Preprod-indekserer.
8. Test registrering, verifisering, tilbakekalling, omstart, duplikatforsøk og
   utilgjengelig proof server før esense får sende ekte dokumentkvitteringer.

## Stoppkriterier

Piloten skal ikke gå videre dersom privat innhold kan avledes fra
forpliktelsen, lommeboknøkkelen må ligge i webprosessen, proof server eksponeres
offentlig, transaksjoner ikke kan verifiseres uavhengig, eller brukerne ikke har
en tydelig nytte av forankringen.

## Bruk av midskills

`midskills.sevryn.xyz` kan hjelpe med å dele arbeidet i sjekklister for Compact,
lommebok, leverandører, testing, utrulling og sikkerhet. Hvert steg skal
verifiseres mot gjeldende offisiell Midnight-dokumentasjon og låses til kjente
versjoner før det kjøres på serveren. Ingen tredjepartsferdighet får lese
esense-data, lommebokfrø eller produksjonshemmeligheter.

Offisielle kilder:

- https://docs.midnight.network/guides/run-proof-server
- https://docs.midnight.network/examples/dapps/bboard

## Hackathon-avgrensning

Hackathon-bidraget skal vise én syntetisk jobb som en enkel, veiledet flyt. Bare
aktivt steg vises. Brukeren går videre med `Fortsett` og kan gå tilbake til
tidligere steg:

1. Oppdrag
2. Planlegg og forbered
3. Krav og faglige hensyn
4. Innsending og vurdering
5. Dokumentasjon og overlevering

Steg 1-4 skal være nyttige uten Midnight. Steg 5 er demonstrasjonens tekniske
poeng: privat dokumentinnhold, en saltet dokumentforpliktelse, bekreftet
Midnight-forankring, uavhengig kontroll og formålsavgrenset tilgang. Dette gjør
Midnight til løsningen på et konkret overleveringsproblem, ikke til generell
dekorasjon eller dokumentlagring.

Den syntetiske demonstrasjonen skal kunne nullstilles og kjøres på norsk og
engelsk. Den skal ikke inneholde ekte elev-, kunde-, bolig- eller måledata. En
arkivklar eksport kan vises som mulig fremtidig grensesnitt mot Boligmappa eller
andre eiendomsarkiv, men ingen eksisterende integrasjon skal påstås.

Utvikling og visuell kontroll skjer lokalt eller i et separat testmiljø.
`esense.no` beholdes som stabil produkttjeneste og oppdateres først når en
kontrollert versjon er klar. Før innlevering må arrangørens regler avklare hvor
mye eksisterende kode som kan inngå, og hvilken ny modul eller demonstrasjon
som må bygges i selve hackathon-perioden.
