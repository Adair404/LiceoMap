-- =========================================================
-- Migración 003: datos de prueba ampliados (GENERADO)
-- Generado por database/tools/generar_datos_prueba.py. Solo datos sintéticos.
-- 4 cursos (1F, 1G, 2A, 2B) con 30 alumnos cada uno, personal por rol,
-- horario semanal completo sin choques y anuncios. Requiere 001 y 002.
-- Credenciales de prueba: docs/datos_prueba.md
-- =========================================================
USE colegio_db;

-- Usuarios nuevos (el rol se resuelve por nombre)
INSERT INTO usuarios (rut, password_hash, nombre, apellido, email, id_rol)
SELECT v.rut, v.hash, v.nombre, v.apellido, v.email, r.id_rol FROM (
    SELECT '13456789-9' AS rut, '$2b$10$GyyRDUJUsY/Hg1/WdbmEX./0gMaDk3nbZxSv5H7SZFgQOiFnzHT1S' AS hash, 'Héctor' AS nombre, 'Carrasco Lagos' AS apellido, 'hector.carrasco@liceomap.test' AS email, 'utp' AS rol
    UNION ALL SELECT '14234567-6', '$2b$10$7yxiStf5KMmQkLoyyX9mrOXPdCrty2yGH2CDZpdf4fi.b3IW6mdf.', 'Rosa', 'Valenzuela Mena', 'rosa.valenzuela@liceomap.test', 'inspectoria'
    UNION ALL SELECT '12876543-3', '$2b$10$/9cEDFLdA3BBVYNbCJo0ROu1ApRBPvn39mbmbgxHv8XytVIn7N0g6', 'Roberto', 'Muñoz Parra', 'roberto.munoz@liceomap.test', 'profesor'
    UNION ALL SELECT '15345678-K', '$2b$10$ZwSOvARftgD039lcuDK/iOyQFYjWP.kwtNsFhYOm1FnL8eApMRIl.', 'Carolina', 'Pizarro Ibáñez', 'carolina.pizarro@liceomap.test', 'profesor'
    UNION ALL SELECT '13987654-7', '$2b$10$XARi8y/ijv2r46Or0g9Tnu9/BhOtNIHyvGsWyfYdRfPhT/xUgwdKu', 'Felipe', 'Araya Sandoval', 'felipe.araya@liceomap.test', 'profesor'
    UNION ALL SELECT '14765432-4', '$2b$10$m.X5XltaGUs//1DQW5rWTO9JQtxAsjU1jK9OV9YV/PJH.hZ3SBUhC', 'Patricia', 'Leiva Rivas', 'patricia.leiva@liceomap.test', 'profesor'
    UNION ALL SELECT '12654321-2', '$2b$10$o/gL.BkSfgfaIuyjsoN4neNpigZOPJ/lHIdwsOAgaJD6kR6svXPSm', 'Sergio', 'Contreras Toro', 'sergio.contreras@liceomap.test', 'profesor'
    UNION ALL SELECT '23836685-2', '$2b$10$zef0VUc1M6FrDADeOtqm1OILv.aJksRkCzHWnK7XI5oJlDfJL8nIi', 'Fernanda', 'Reyes Bravo', 'fernanda.reyes@liceomap.test', 'alumno'
    UNION ALL SELECT '23883594-1', '$2b$10$IgfT7YuczpFgD/px7vIZe.uq1uKgOYmwTpMtya6DjAFtotP5emOz6', 'Rodrigo', 'Contreras Fuentes', 'rodrigo.contreras@liceomap.test', 'alumno'
    UNION ALL SELECT '23814750-6', '$2b$10$Ua9aOPcxJrvOvMeQ9z.vte69TyRh7EP79Ctmbtk14fpNJK6sEqV8q', 'Vicente', 'Leiva Pizarro', 'vicente.leiva@liceomap.test', 'alumno'
    UNION ALL SELECT '23302657-3', '$2b$10$L4B6sFbxCZuQZT/2hKqsI.VFaw70NBicBcavPAgTdsDvYpIqwt7pa', 'Ignacio', 'Carrasco Hernández', 'ignacio.carrasco@liceomap.test', 'alumno'
    UNION ALL SELECT '23601193-3', '$2b$10$WJUA8CwH8Jslmj7U.5IVC.qbfcEfjyidHZw/QrLy1GQVQJe2h3f6i', 'Bastián', 'Soto Silva', 'bastian.soto@liceomap.test', 'alumno'
    UNION ALL SELECT '23814102-8', '$2b$10$eUoF8yK0K8PTrVGBTk0UZ.DCekwFLSggTgcyKUrA0ipmKArXeXUvG', 'Javiera', 'Carrasco González', 'javiera.carrasco@liceomap.test', 'alumno'
    UNION ALL SELECT '23716512-8', '$2b$10$8Vbsug7mdhiLIzpuXiIY1edMihrYLwIVPnGmT4jjPlb6udOgO7BrG', 'Esteban', 'Reyes Araya', 'esteban.reyes@liceomap.test', 'alumno'
    UNION ALL SELECT '23694625-8', '$2b$10$.sgbwP4mU.b3G4Dmh2HiaOsG2dMz/DWssMukCeJNXaU9ZE9Mm03Uq', 'Daniela', 'Tapia Tapia', 'daniela.tapia@liceomap.test', 'alumno'
    UNION ALL SELECT '23380027-9', '$2b$10$9N5ju7eec/naildXcqY41eV1iZzYW6r1pHHDUCutVti09V1NQU03y', 'Gonzalo', 'Bravo Jara', 'gonzalo.bravo@liceomap.test', 'alumno'
    UNION ALL SELECT '23884529-7', '$2b$10$S0OO0zZjb9GID4g5pBxmJeIhyakA50IAfqeOVGZgH2A4l1Tu1C.Aq', 'Ángel', 'Gutiérrez Soto', 'angel.gutierrez@liceomap.test', 'alumno'
    UNION ALL SELECT '23779668-3', '$2b$10$krNGibnAcHsukSXhibeVXOFPO7ZFX4qwJZmp8Bt6W89R8mK16iCl6', 'Lucas', 'Vásquez Vásquez', 'lucas.vasquez@liceomap.test', 'alumno'
    UNION ALL SELECT '23624008-8', '$2b$10$A50Q9w1JDg8y7wZwVK3Pl.TfbyDOsMS7WucaD3jFZeEC8getJB9jG', 'Francisca', 'Aguilera Medina', 'francisca.aguilera@liceomap.test', 'alumno'
    UNION ALL SELECT '23681201-4', '$2b$10$S2SVFXeO2TCeai5977AIUuUlix577e1T7.f.Ai8U8J0yEmlTLrML2', 'Valentina', 'Medina Campos', 'valentina.medina@liceomap.test', 'alumno'
    UNION ALL SELECT '23718144-1', '$2b$10$OMlaws/4pCNcQgaIq6FJ8.rO3WS0SeNllVg9E.2LXZfsO0p79Bgpu', 'Tomás', 'Riquelme Soto', 'tomas.riquelme@liceomap.test', 'alumno'
    UNION ALL SELECT '23422104-3', '$2b$10$rd2uH1QYY2st6tMAEDKNeOPztAFKFH.RBoXiid.E2Yl4uaw4zaUsm', 'Ignacio', 'Pizarro Cáceres', 'ignacio.pizarro@liceomap.test', 'alumno'
    UNION ALL SELECT '23814883-9', '$2b$10$SC.ZrLK5zKtR6w38UhLPm..Nx2Ac1BJQmHmx7K6fhguQngwvD2rpS', 'Martín', 'Bravo Ortiz', 'martin.bravo@liceomap.test', 'alumno'
    UNION ALL SELECT '23740366-5', '$2b$10$vvHa17kvetidhv1dJ9VAneaWaeN57JurKd7eXt9RFlRKUzWao8XxW', 'Benjamín', 'Molina Torres', 'benjamin.molina@liceomap.test', 'alumno'
    UNION ALL SELECT '23843148-4', '$2b$10$JwWSYRxoxiOiPICWp427de9A0MUbfG6d5/WBK.4JwzQwajU/eRLKm', 'Felipe', 'Álvarez Bravo', 'felipe.alvarez@liceomap.test', 'alumno'
    UNION ALL SELECT '23435265-2', '$2b$10$D1mMBJphTZafEOjrqNHP0OLFaw2qqeBJh2uYC/GX9N8yA2Js7KQ2O', 'Valentina', 'Leiva Fuentes', 'valentina.leiva@liceomap.test', 'alumno'
    UNION ALL SELECT '23407559-4', '$2b$10$zpDHLDJNjtdLi7Mw8TrVv.nkot7IYEE7s7zEXro9mADMyr0JgcQuq', 'Isidora', 'Medina Molina', 'isidora.medina@liceomap.test', 'alumno'
    UNION ALL SELECT '23792873-3', '$2b$10$l0ePhD1kTRMpZZFzihVnQuAXzPImiEtl3l9amTWKI8rLPHq3Ug8Ma', 'Alonso', 'Navarro Riquelme', 'alonso.navarro@liceomap.test', 'alumno'
    UNION ALL SELECT '23427940-8', '$2b$10$yNSDh9SIONZnTkh1L2M8AOpjPng44D57y63wrpLc9DpONjIkiexiC', 'Francisca', 'Álvarez Fuentes', 'francisca.alvarez@liceomap.test', 'alumno'
    UNION ALL SELECT '23792207-7', '$2b$10$xn6lhVoCBr3RZ7PzygDQHO.AYltVpCSXAlnLCuhPzgq0NNSNJGKfi', 'Álvaro', 'Salazar Vera', 'alvaro.salazar@liceomap.test', 'alumno'
    UNION ALL SELECT '23886988-9', '$2b$10$NHAnzFmkQZKY.s8v0npyheb//TxAwSjqVJkV.VWv75OIyez0uuFn.', 'Alonso', 'Valenzuela Torres', 'alonso.valenzuela@liceomap.test', 'alumno'
    UNION ALL SELECT '23874775-9', '$2b$10$UehSgUDpeESH7NAKMZX5uuWZH/TClkHCyUZTvFMvKcN5iO4vQKVXe', 'Benjamín', 'Godoy Castillo', 'benjamin.godoy@liceomap.test', 'alumno'
    UNION ALL SELECT '23802155-3', '$2b$10$/0tfh/hKsqR493olwJW4o.AVG21AcBhyHtMfYv/rPdaampwCkgvUa', 'Rodrigo', 'Bravo Salazar', 'rodrigo.bravo@liceomap.test', 'alumno'
    UNION ALL SELECT '23608673-9', '$2b$10$oZibEJcrB7cTb94QCmAk5uoXj54Xl1ksiG4iu8JwEXMBlPkChL6fO', 'Benjamín', 'Riquelme López', 'benjamin.riquelme@liceomap.test', 'alumno'
    UNION ALL SELECT '23457122-2', '$2b$10$Glq5nLxKQNuHgK1gJDlxGeunprjgg8lz5qMv8fy4b7/AEd7bMdVGu', 'Camila', 'González Rojas', 'camila.gonzalez@liceomap.test', 'alumno'
    UNION ALL SELECT '23848288-7', '$2b$10$65GRLoIkUUrPvpOSF94R4ejI0buv/x1HQ1o7jaby/FJ1SOrH78C/6', 'Rodrigo', 'Ortiz Vera', 'rodrigo.ortiz@liceomap.test', 'alumno'
    UNION ALL SELECT '23572745-5', '$2b$10$AL0iyjqSbZ6/0c9O17jgGuZ0iQQf5ZdX/0DWSve1x9xsouq2P1IC6', 'Cristóbal', 'Campos López', 'cristobal.campos@liceomap.test', 'alumno'
    UNION ALL SELECT '23836102-8', '$2b$10$XLasKiu3GNovbis2OYcMEuTWan5wv9oZ2RzGugk057iC/fRgErXA.', 'Cristian', 'Cáceres Vera', 'cristian.caceres@liceomap.test', 'alumno'
    UNION ALL SELECT '23335253-5', '$2b$10$aIMyw1GuwDdLPlm1hFPNBe4yn9iaykv18UYphPRIEFcFw0MczWX4C', 'Cristóbal', 'Riquelme Pizarro', 'cristobal.riquelme@liceomap.test', 'alumno'
    UNION ALL SELECT '23403152-K', '$2b$10$Ni5wgsEW1eHES.yCinVyyeDJsLiKn32Bq0b5LnKHpBcOeGZqGhAAC', 'Trinidad', 'Reyes Vera', 'trinidad.reyes@liceomap.test', 'alumno'
    UNION ALL SELECT '23840198-4', '$2b$10$/xzZ3Xg.YQTUN6odJMsCTOH9VrZ9sRiceYsV6AAgPAKEEZJZzJXE.', 'Joaquín', 'Salazar Medina', 'joaquin.salazar@liceomap.test', 'alumno'
    UNION ALL SELECT '23746459-1', '$2b$10$3vsdkk98TcUC3ThzEyhluu2tuSxAnyZQL4BhQbkMNkpexHZvPoun6', 'Daniela', 'Carrasco Rodríguez', 'daniela.carrasco@liceomap.test', 'alumno'
    UNION ALL SELECT '23579409-8', '$2b$10$Xz7frxIwIgA6j4VMRkUgAuwXj/FuslypscIDFPa1185.PYpRulgES', 'Ángel', 'Álvarez Pérez', 'angel.alvarez@liceomap.test', 'alumno'
    UNION ALL SELECT '23504038-7', '$2b$10$QmFQl7O3xppzpl5L0onqiOXq/lizD/.0QIL6PX9svdY2i1I6gpZ06', 'Cristóbal', 'Campos Contreras', 'cristobal.campos2@liceomap.test', 'alumno'
    UNION ALL SELECT '23771224-2', '$2b$10$JjkTh5fIyMPeMn1i9.Btb.AqCEQUco.JItpn5vY.6Cq8/2n0kQeSK', 'Gonzalo', 'Figueroa Sepúlveda', 'gonzalo.figueroa@liceomap.test', 'alumno'
    UNION ALL SELECT '23773149-2', '$2b$10$r/uUyfHgEOo4l/RWE8C08uixoS6zkHOYHfuKoOGah2Kzkkn4BBFLq', 'Sofía', 'Soto González', 'sofia.soto@liceomap.test', 'alumno'
    UNION ALL SELECT '23508448-1', '$2b$10$68KwRu0o064khJ.zcyVX5OKp2pbA77HgHPipoJwzR7YMamzlF5JyG', 'Ignacio', 'Valenzuela Soto', 'ignacio.valenzuela@liceomap.test', 'alumno'
    UNION ALL SELECT '23346828-2', '$2b$10$2t6PO9wDGXkDsafgFS.JxuUkQT0pfabHnT8YYVXKlDfujSXlSJjqa', 'Emilia', 'Silva Navarro', 'emilia.silva@liceomap.test', 'alumno'
    UNION ALL SELECT '23674604-6', '$2b$10$Pp/GnaueXlJbPkPx.rbaMeIgJDP9jal9DzCSdguYuCxyblby1j0KK', 'Lucas', 'Espinoza Godoy', 'lucas.espinoza@liceomap.test', 'alumno'
    UNION ALL SELECT '23815887-7', '$2b$10$NkSvMyTyZ5g5mId/NDnXB.GahO19wvH7uEvXJuc0rXOq36AelZoDe', 'Francisca', 'González Reyes', 'francisca.gonzalez@liceomap.test', 'alumno'
    UNION ALL SELECT '23533756-8', '$2b$10$oRImbyddtcyUMzrQxu/7q.Sls.GUuzcXpc2.2UUiw0ZgiE35fYBWO', 'Cristian', 'Martínez Valenzuela', 'cristian.martinez@liceomap.test', 'alumno'
    UNION ALL SELECT '23829238-7', '$2b$10$l98YjN/TgnJQSVw1YUKVlO9WlQpyvdwFfS3W53GHp6nyIaMk2g/HK', 'Sebastián', 'Guzmán Martínez', 'sebastian.guzman@liceomap.test', 'alumno'
    UNION ALL SELECT '23467899-K', '$2b$10$6sR/P79VgZvwHL.qY7r/4uaOYUI/HFz7iODgOco36EiHT/8AaOrWe', 'Trinidad', 'Soto Figueroa', 'trinidad.soto@liceomap.test', 'alumno'
    UNION ALL SELECT '23832364-9', '$2b$10$fWs65TpK/6MOsx/MOseTcOckabvlMciU.zRLWE4jDL4J46LYGx1fa', 'Constanza', 'Guzmán Castillo', 'constanza.guzman@liceomap.test', 'alumno'
    UNION ALL SELECT '23845291-0', '$2b$10$eCswNcGK0IiOAY46XfrWCukdFNHBp40BXLbMuIOER/.1DQGerjAIC', 'Vicente', 'Cortés Sepúlveda', 'vicente.cortes@liceomap.test', 'alumno'
    UNION ALL SELECT '23411289-9', '$2b$10$JNI2cm0RFm0RaHF6IBzG1uiJPAmwJo3aygSrhnxB8TrrF6XIZadYG', 'Renata', 'Cortés González', 'renata.cortes@liceomap.test', 'alumno'
    UNION ALL SELECT '23663874-K', '$2b$10$H2cEshefR8X/sNsw0vA56OV1BuuvqNWrARWeb2u/Z32Dm8cVj8rUO', 'Matías', 'Pérez Díaz', 'matias.perez@liceomap.test', 'alumno'
    UNION ALL SELECT '23326824-0', '$2b$10$HLJJdFdEF3IIeTHvGhhYS.XjwBOIB2FDNdKQQV7M8R.qy4LueFhp.', 'Rodrigo', 'Tapia Muñoz', 'rodrigo.tapia@liceomap.test', 'alumno'
    UNION ALL SELECT '23618422-6', '$2b$10$GpnidlCPWVcWXNrR5A4g0uwwALz60Au0jcuvSO1qITPsMoH3gaO8G', 'Maximiliano', 'Álvarez Reyes', 'maximiliano.alvarez@liceomap.test', 'alumno'
    UNION ALL SELECT '23821739-3', '$2b$10$hYGRiXX0WDpkNv9qs6fbh.mFX2xpUKeDfary9J91g1t44oxbQoS.O', 'Joaquín', 'Reyes Silva', 'joaquin.reyes@liceomap.test', 'alumno'
    UNION ALL SELECT '23479027-7', '$2b$10$yuOfuRdENfmxy0WUAIf6bOrqOzkM0lH85DjNgEIDCN.0pTOuQ8vMi', 'Tomás', 'Leiva Navarro', 'tomas.leiva@liceomap.test', 'alumno'
    UNION ALL SELECT '23517040-K', '$2b$10$VGicH4Ootsu4J97w5ypjLOtsEZJWbxSaDy0iyKI0uC.qOo0/oYsBe', 'Francisca', 'Guzmán Molina', 'francisca.guzman@liceomap.test', 'alumno'
    UNION ALL SELECT '23781104-6', '$2b$10$2ZNWknZONe/me1.yRieW5uDeHE15ex/wOenI5x078XQo6BaBmkz7G', 'Martín', 'Navarro Gutiérrez', 'martin.navarro@liceomap.test', 'alumno'
    UNION ALL SELECT '23372884-5', '$2b$10$LmHHrud6mqVHHnkQDKvSY.nBht1IzGT4kyspBT.b6tWnDEZlcqe7e', 'Gabriel', 'Fuentes Orellana', 'gabriel.fuentes@liceomap.test', 'alumno'
    UNION ALL SELECT '23504990-2', '$2b$10$lcY.Ygjb9pxpt5G1pTwtAO2/iHcvJOIiICPHFIyHxbthN.K0dT8Fi', 'Diego', 'Núñez Rojas', 'diego.nunez@liceomap.test', 'alumno'
    UNION ALL SELECT '23871229-7', '$2b$10$SLLMdHu.BSRckAodpOvf3OnR8zY0prlY6J3Yl2sRkTx6Hx9Cb8pn2', 'Rodrigo', 'Rodríguez Rojas', 'rodrigo.rodriguez@liceomap.test', 'alumno'
    UNION ALL SELECT '22697687-6', '$2b$10$3lz6aNW3UL.p.pszFNyEBelXx/v2TxBJtkNFLvxkmBeD0NOn9664C', 'Isidora', 'Carrasco Aguilera', 'isidora.carrasco@liceomap.test', 'alumno'
    UNION ALL SELECT '22521464-6', '$2b$10$Z7coLszPbfwoUP3bTsYvfeN8cf0UzN83AEmFkZH4vrN7NwF8RvCVm', 'Sebastián', 'Medina Orellana', 'sebastian.medina@liceomap.test', 'alumno'
    UNION ALL SELECT '22729348-9', '$2b$10$1Homygnxer901SMy4DUekurD/TGU9a3t7x1A/n8x8CkdD0lO3IsFO', 'Constanza', 'Aguilera Molina', 'constanza.aguilera@liceomap.test', 'alumno'
    UNION ALL SELECT '22695040-0', '$2b$10$H/QYKvIquvKSA6tmHfJgMeX9ptmkYdK/9xEcMR5WKNYhN4yaHw5zO', 'Nicolás', 'Martínez Morales', 'nicolas.martinez@liceomap.test', 'alumno'
    UNION ALL SELECT '23058902-K', '$2b$10$.Fmgh7IX0AycDc.eDa9lEeZigu0xCMqJCV1hcQQ/LoCMduwcxKCdS', 'Matías', 'Espinoza Riquelme', 'matias.espinoza@liceomap.test', 'alumno'
    UNION ALL SELECT '22819720-3', '$2b$10$bRDOuLXEWibdsPTxM3rdbukuPLmY.5dzLVAmpA10iXKY5RgzUQrYG', 'Vicente', 'Soto Cortés', 'vicente.soto@liceomap.test', 'alumno'
    UNION ALL SELECT '22776240-3', '$2b$10$QadvATptqgNkNSUgctcscuc4QQ703eowCdtmvWFJXxzYIsGhP42nO', 'Florencia', 'Tapia Rodríguez', 'florencia.tapia@liceomap.test', 'alumno'
    UNION ALL SELECT '22801644-6', '$2b$10$7iidTE4odCj6DWmQ7NaHkuJSzXs6F7SLVUUlrGMP6FPvyiBo/2Ax.', 'Tomás', 'Cáceres Figueroa', 'tomas.caceres@liceomap.test', 'alumno'
    UNION ALL SELECT '23044562-1', '$2b$10$zziFRYaLqj4W0pbGV.9TXeTK2GdL1.SQPYVUZsZiSJjWV5./HMYZW', 'Tomás', 'Rodríguez Reyes', 'tomas.rodriguez@liceomap.test', 'alumno'
    UNION ALL SELECT '23052863-2', '$2b$10$/bZ46CXKrNTxsSsETNBr9etEHObUQvqi52Gjyt6pcUMS/6lopZA2q', 'Sebastián', 'Carrasco Silva', 'sebastian.carrasco@liceomap.test', 'alumno'
    UNION ALL SELECT '22724742-8', '$2b$10$Ozu9GOAvvoYSS/9ADEtUvOAriIhhEEx8rKvWUYPj7pBuTLsqlWkOG', 'Nicolás', 'Espinoza Contreras', 'nicolas.espinoza@liceomap.test', 'alumno'
    UNION ALL SELECT '22976172-2', '$2b$10$1IYtZgAe8tuYicDHchfi1.bihWyr58Uy6iTZyvewoMZVn1txHH0mu', 'Agustina', 'González Soto', 'agustina.gonzalez@liceomap.test', 'alumno'
    UNION ALL SELECT '23071536-K', '$2b$10$Ab7Z/o1N05HThtqIfXofzutBq0L.Iutw5GFJE5by6Oe5kgHV7d/Rq', 'Rodrigo', 'Gutiérrez Figueroa', 'rodrigo.gutierrez@liceomap.test', 'alumno'
    UNION ALL SELECT '22869046-5', '$2b$10$8G1LSA.ZSiOWyCF2zZ6oWevQozu/onWRARl1O/STbC0vWrsETGLfC', 'Franco', 'Rodríguez Muñoz', 'franco.rodriguez@liceomap.test', 'alumno'
    UNION ALL SELECT '23064531-0', '$2b$10$kJ6TW35FJA8RopS.gNT9r.r0dzOn0/lkn4m2judFVPTtfQ7smxLlu', 'Amanda', 'Tapia Pizarro', 'amanda.tapia@liceomap.test', 'alumno'
    UNION ALL SELECT '22794096-4', '$2b$10$QFsocSYpNPGT1L3Az1hRtOSiKAPgx7GawPXNpY2dg6ZJBMb00JLSG', 'Josefa', 'Silva Navarro', 'josefa.silva@liceomap.test', 'alumno'
    UNION ALL SELECT '23097515-9', '$2b$10$viwwd0nA/vqSz2iiZLMA1u6ZP13i8EgssT8i9Uk5gHxqQqlNVMVl2', 'Diego', 'Leiva Araya', 'diego.leiva@liceomap.test', 'alumno'
    UNION ALL SELECT '23082729-K', '$2b$10$CcLitQHAEC0bATa2P5yrv.gx9lHFJQfzNVR0BdF6Ywc1vZsrJtXsG', 'Trinidad', 'Leiva Espinoza', 'trinidad.leiva@liceomap.test', 'alumno'
    UNION ALL SELECT '22601114-5', '$2b$10$41u.rdBcQDUUejpqAMhObOZeFLF6ORFE6K8dGnY5PoHFKSgOoyGsG', 'Constanza', 'Contreras Torres', 'constanza.contreras@liceomap.test', 'alumno'
    UNION ALL SELECT '22563361-4', '$2b$10$u3J16.n0BuUGqaYf9JSDNu1CgPwluq3xv4TwJuPCEPN6xJ5O8oHPO', 'Martín', 'Morales Contreras', 'martin.morales@liceomap.test', 'alumno'
    UNION ALL SELECT '22611484-K', '$2b$10$yIPrp6/zrViJMq4kK9egY.FnM8aht0xGyeJ.PEIYo0UxaYfy.2lgC', 'Ignacia', 'Rodríguez Aguilera', 'ignacia.rodriguez@liceomap.test', 'alumno'
    UNION ALL SELECT '22567019-6', '$2b$10$NhapVwymxAmNTq3tISljfudYNQ74c4nK6xGxShaTTPg1uzkv6Iv/y', 'Maximiliano', 'Reyes Espinoza', 'maximiliano.reyes@liceomap.test', 'alumno'
    UNION ALL SELECT '22773529-5', '$2b$10$WWXexJyxE5xXF0x2YKl1cui1eWcYW.AVW9ULPEAXBYPtCUV8mPsIq', 'Trinidad', 'Reyes Morales', 'trinidad.reyes2@liceomap.test', 'alumno'
    UNION ALL SELECT '22931638-9', '$2b$10$GQyFIkkjNU.kBdtm163Cvu.GWfa16gpvqCoXL5fRSEBMRc7P298Z6', 'Daniela', 'Pérez González', 'daniela.perez@liceomap.test', 'alumno'
    UNION ALL SELECT '22560095-3', '$2b$10$w1mcBJ6Zt4KgyEmohSURKuJZI1gjx/iUDO5Y/5Mg9Aqk/GRu7xdx2', 'Daniela', 'Figueroa González', 'daniela.figueroa@liceomap.test', 'alumno'
    UNION ALL SELECT '22824973-4', '$2b$10$jbRJELjvNK5g5kInafe1Wet.u878gFVi05CSvSWU3lhRH.3YluGvW', 'Javiera', 'Hernández Muñoz', 'javiera.hernandez@liceomap.test', 'alumno'
    UNION ALL SELECT '23088438-2', '$2b$10$4XSlxVpv7WURHhrDwafSFeflLKXkl5as0VnqFEOlVuI9ASP2KdZjO', 'Fernanda', 'Contreras Orellana', 'fernanda.contreras@liceomap.test', 'alumno'
    UNION ALL SELECT '22978197-9', '$2b$10$2gXFqtSodegQBbkUCul9kegGHJTabVXb/S4Tr/s6Uv.jp3gbDHCaq', 'Felipe', 'Tapia Reyes', 'felipe.tapia@liceomap.test', 'alumno'
    UNION ALL SELECT '22539857-7', '$2b$10$uz15C6vak0.ODBpixkX9wOe.aJIah5DF5MYQbyeNZUUS9ohgCQe1.', 'Gabriel', 'Jara Aguilera', 'gabriel.jara@liceomap.test', 'alumno'
    UNION ALL SELECT '22726110-2', '$2b$10$AMLtJtz68sT6ufV780SeX.PM.vPkVO386oGjj9mZkSBO2njTBz03O', 'Benjamín', 'Reyes Ortiz', 'benjamin.reyes@liceomap.test', 'alumno'
    UNION ALL SELECT '22625242-8', '$2b$10$jXzihkLzofWd46emBU9b9Orh.YpsyPEZczhG3lQHB8C2MPSo6YS3C', 'Gabriel', 'Vera Riquelme', 'gabriel.vera@liceomap.test', 'alumno'
    UNION ALL SELECT '22763798-6', '$2b$10$/39ybYJdpIYgkKfR5d54hOF19rz7yGzJNeS3cjt7t02W1ZCXXcrMu', 'Esteban', 'Campos Bravo', 'esteban.campos@liceomap.test', 'alumno'
    UNION ALL SELECT '22560430-4', '$2b$10$4RQSwkBBFhU1hcd6/v9NNeiBeJSRkSNXMQlL4rvdmAsKcWzQJR./i', 'Matías', 'Vásquez Tapia', 'matias.vasquez@liceomap.test', 'alumno'
    UNION ALL SELECT '22524812-5', '$2b$10$.AxrPwueaFtr.bg5x5eduuUIHvzjE9RjXWqdXCBHKOWdEIok7bORO', 'Gonzalo', 'Medina Riquelme', 'gonzalo.medina@liceomap.test', 'alumno'
    UNION ALL SELECT '22803621-8', '$2b$10$ap1kxBZ1jNXLhScSdzbr4uyVD4jNoXyb5GPSKIa7XUefFQuD4a6gW', 'Trinidad', 'Salazar Gutiérrez', 'trinidad.salazar@liceomap.test', 'alumno'
    UNION ALL SELECT '22936875-3', '$2b$10$V3.hiP820I24d8NV9f8kZelHhfIWTMda8M/6YQsT11YZzu9ltVkJS', 'Ángel', 'Silva Castillo', 'angel.silva@liceomap.test', 'alumno'
    UNION ALL SELECT '23068492-8', '$2b$10$d8IDsq/FT2VzdhRpMn49PO.5fy/c9PxreP32Ttz25U0Zi3i0Is9n6', 'Rocío', 'Guzmán Muñoz', 'rocio.guzman@liceomap.test', 'alumno'
    UNION ALL SELECT '22558872-4', '$2b$10$qz3T3xkf3DPl4Wsys7BUa.4zUJ9n.XWBhmTktA3vMvK19OWOAV2Sq', 'Bárbara', 'López Pizarro', 'barbara.lopez@liceomap.test', 'alumno'
    UNION ALL SELECT '22628644-6', '$2b$10$Z/DRLKInj05jUhh7F0FRhuPJX9AGxB4fSjfNL9rQpAGGrVJdV6kdi', 'Ángel', 'Silva Morales', 'angel.silva2@liceomap.test', 'alumno'
    UNION ALL SELECT '23047968-2', '$2b$10$dirGDazMkVJ2Zjs.WkktUep0UhOC.4pzvS6gp/V.iOCuuTMib7Dxe', 'Fernanda', 'Rojas Martínez', 'fernanda.rojas@liceomap.test', 'alumno'
    UNION ALL SELECT '22816922-6', '$2b$10$16oesWKs9Lb4xscRDfODxOEEoyYTsIwqs1hhGxyXI6F.QbfWoqzuW', 'Ignacia', 'Ortiz Aguilera', 'ignacia.ortiz@liceomap.test', 'alumno'
    UNION ALL SELECT '22632432-1', '$2b$10$jUBcz54mQbz4DfVY1jbQzumU5IaSuACSPm8VORhg7Qh2mlNi2BDE2', 'Valentina', 'Riquelme Guzmán', 'valentina.riquelme@liceomap.test', 'alumno'
    UNION ALL SELECT '22895504-3', '$2b$10$Q0yy1ZkdKUe/fBRVC/MZCuRf2T3ugQt5av73BCsYcYcQPKa/JDnz.', 'Ignacia', 'Figueroa Cortés', 'ignacia.figueroa@liceomap.test', 'alumno'
    UNION ALL SELECT '22730230-5', '$2b$10$V5tyfJbSPSYpEVGXYRKf6ekbdETPIku4qmzg1lKsRlwebzlTWM5YS', 'Emilia', 'Figueroa Godoy', 'emilia.figueroa@liceomap.test', 'alumno'
    UNION ALL SELECT '22529797-5', '$2b$10$kkL.jmSjOWgOlHNOYT2BEOdvmmTXci2eEF1HPyxdtmuts7CCv4Fuy', 'Constanza', 'Rodríguez Valenzuela', 'constanza.rodriguez@liceomap.test', 'alumno'
    UNION ALL SELECT '23081852-5', '$2b$10$rSDTZCyfsBKZd8qu7oJwK.9y4Es.wcfWsp.blDrmed.G6p4W9KEQW', 'Franco', 'Medina Valenzuela', 'franco.medina@liceomap.test', 'alumno'
    UNION ALL SELECT '22739343-2', '$2b$10$wgTF9O5XObzFW7ZzWfWUUufdvo6w5xsIzYjcICEQePbsp18rzm8Yy', 'Benjamín', 'Torres Sepúlveda', 'benjamin.torres@liceomap.test', 'alumno'
    UNION ALL SELECT '23067436-1', '$2b$10$DNnWYKXOxCiLpwOKjwoN/eZU9y9QfxsuwgKwurG91bcHuUQtkSuT.', 'Valentina', 'Muñoz Espinoza', 'valentina.munoz@liceomap.test', 'alumno'
    UNION ALL SELECT '22830033-0', '$2b$10$FLM2eCfuOZomlSBFxz3Zu.drdG/r5dNgOCXMeupW4sdcu/Cw.1Fwm', 'Sebastián', 'Figueroa Torres', 'sebastian.figueroa@liceomap.test', 'alumno'
    UNION ALL SELECT '22593791-5', '$2b$10$WnenNUBMtw1EANz7gE22ce3qdn/f5qQBFqVK/B4ICIaDSiVOkSYnu', 'Constanza', 'Jara Guzmán', 'constanza.jara@liceomap.test', 'alumno'
    UNION ALL SELECT '23039017-7', '$2b$10$qIfjKr49vf3fm8CJvfXcN.ACPoQrX/qF1sylHtbJsiVK2Deuo2ZGq', 'Florencia', 'Pizarro Rojas', 'florencia.pizarro@liceomap.test', 'alumno'
    UNION ALL SELECT '23045730-1', '$2b$10$X8pivUuQYZm8jtDDbe6HFuprnrn5nt95Upg3ORleZVBR7JfrxmbkW', 'Daniela', 'Gutiérrez Jara', 'daniela.gutierrez@liceomap.test', 'alumno'
    UNION ALL SELECT '22511963-5', '$2b$10$aKt4WMRlq7u36tePn0vKLuZVaJUpm2PPDqywJ1LC97Q6zg.pG7LTW', 'Gonzalo', 'Reyes Díaz', 'gonzalo.reyes@liceomap.test', 'alumno'
    UNION ALL SELECT '22561128-9', '$2b$10$5619/Z8myVklNvidpYOIseRUokuy4wecAh4tQFFVUG0tSYnxMdKT6', 'Álvaro', 'Hernández Álvarez', 'alvaro.hernandez@liceomap.test', 'alumno'
    UNION ALL SELECT '22658174-K', '$2b$10$cEF/25R3tHMrKrL.qvNhkuWcC0GNW5307obpG5wv4mPLNc8d3/wpK', 'Agustina', 'Orellana Bravo', 'agustina.orellana@liceomap.test', 'alumno'
    UNION ALL SELECT '22877415-4', '$2b$10$uw.m7rCmir4SCv//XS3b/.bFSJ/UeoTTArIg6rH7CpFWm4UEt.KG.', 'Gonzalo', 'Núñez Medina', 'gonzalo.nunez@liceomap.test', 'alumno'
    UNION ALL SELECT '22860382-1', '$2b$10$C1DRG14Y9JBnkw6/WkLO0uL2gFNfw/mJn0qBp4T3hMolFFTezUHIO', 'Agustina', 'Pizarro Espinoza', 'agustina.pizarro@liceomap.test', 'alumno'
    UNION ALL SELECT '22981577-6', '$2b$10$7QjU.R682/xc7ebfuw01deLgTD6nXJ2avoIeJJGRKSxQaxZrF.zaO', 'Renata', 'Campos Tapia', 'renata.campos@liceomap.test', 'alumno'
) v JOIN roles r ON r.nombre = v.rol;

-- Correos de los usuarios creados en la migración 002
UPDATE usuarios SET email = 'daniel.creador@liceomap.test' WHERE rut = '20100001-7';
UPDATE usuarios SET email = 'marta.rojas@liceomap.test' WHERE rut = '20100002-5';
UPDATE usuarios SET email = 'pablo.soto@liceomap.test' WHERE rut = '20100003-3';
UPDATE usuarios SET email = 'juan.carlos@liceomap.test' WHERE rut = '20100004-1';
UPDATE usuarios SET email = 'ana.fuentes@liceomap.test' WHERE rut = '20100005-K';
UPDATE usuarios SET email = 'jorge.badani@liceomap.test' WHERE rut = '20100006-8';
UPDATE usuarios SET email = 'camila.vega@liceomap.test' WHERE rut = '20100007-6';
UPDATE usuarios SET email = 'diego.torres@liceomap.test' WHERE rut = '20100008-4';

-- Profesores jefe y matrícula (se reemplaza la matrícula de los 4 cursos)
UPDATE cursos SET id_profesor_jefe = (SELECT id_usuario FROM usuarios WHERE rut = '20100004-1') WHERE id_curso = '1F';
UPDATE cursos SET id_profesor_jefe = (SELECT id_usuario FROM usuarios WHERE rut = '15345678-K') WHERE id_curso = '1G';
UPDATE cursos SET id_profesor_jefe = (SELECT id_usuario FROM usuarios WHERE rut = '20100005-K') WHERE id_curso = '2A';
UPDATE cursos SET id_profesor_jefe = (SELECT id_usuario FROM usuarios WHERE rut = '13987654-7') WHERE id_curso = '2B';
DELETE FROM curso_alumno WHERE id_curso IN ('1F', '1G', '2A', '2B');
INSERT INTO curso_alumno (id_curso, id_alumno) SELECT '1F', id_usuario FROM usuarios WHERE rut IN (
    '20100006-8', '23836685-2', '23883594-1', '23814750-6', '23302657-3', '23601193-3', '23814102-8', '23716512-8', '23694625-8', '23380027-9', '23884529-7', '23779668-3', '23624008-8', '23681201-4', '23718144-1', '23422104-3', '23814883-9', '23740366-5', '23843148-4', '23435265-2', '23407559-4', '23792873-3', '23427940-8', '23792207-7', '23886988-9', '23874775-9', '23802155-3', '23608673-9', '23457122-2', '23848288-7'
);
INSERT INTO curso_alumno (id_curso, id_alumno) SELECT '1G', id_usuario FROM usuarios WHERE rut IN (
    '23572745-5', '23836102-8', '23335253-5', '23403152-K', '23840198-4', '23746459-1', '23579409-8', '23504038-7', '23771224-2', '23773149-2', '23508448-1', '23346828-2', '23674604-6', '23815887-7', '23533756-8', '23829238-7', '23467899-K', '23832364-9', '23845291-0', '23411289-9', '23663874-K', '23326824-0', '23618422-6', '23821739-3', '23479027-7', '23517040-K', '23781104-6', '23372884-5', '23504990-2', '23871229-7'
);
INSERT INTO curso_alumno (id_curso, id_alumno) SELECT '2A', id_usuario FROM usuarios WHERE rut IN (
    '20100007-6', '20100008-4', '22697687-6', '22521464-6', '22729348-9', '22695040-0', '23058902-K', '22819720-3', '22776240-3', '22801644-6', '23044562-1', '23052863-2', '22724742-8', '22976172-2', '23071536-K', '22869046-5', '23064531-0', '22794096-4', '23097515-9', '23082729-K', '22601114-5', '22563361-4', '22611484-K', '22567019-6', '22773529-5', '22931638-9', '22560095-3', '22824973-4', '23088438-2', '22978197-9'
);
INSERT INTO curso_alumno (id_curso, id_alumno) SELECT '2B', id_usuario FROM usuarios WHERE rut IN (
    '22539857-7', '22726110-2', '22625242-8', '22763798-6', '22560430-4', '22524812-5', '22803621-8', '22936875-3', '23068492-8', '22558872-4', '22628644-6', '23047968-2', '22816922-6', '22632432-1', '22895504-3', '22730230-5', '22529797-5', '23081852-5', '22739343-2', '23067436-1', '22830033-0', '22593791-5', '23039017-7', '23045730-1', '22511963-5', '22561128-9', '22658174-K', '22877415-4', '22860382-1', '22981577-6'
);

-- Materias
INSERT IGNORE INTO materias (nombre) VALUES ('Matemáticas'), ('Lenguaje'), ('Historia'), ('Inglés'), ('Ciencias Naturales'), ('Educación Física'), ('Electrónica'), ('Computación'), ('Orientación');

-- Horario semanal (reemplaza los horarios de ejemplo anteriores)
DELETE FROM horarios;
INSERT INTO horarios (id_curso, id_materia, id_profesor, id_espacio, id_bloque, dia_semana, hora_inicio, hora_fin)
SELECT h.id_curso, m.id_materia, u.id_usuario, h.id_espacio, b.id_bloque, h.dia, b.hora_inicio, b.hora_fin FROM (
    SELECT '1F' AS id_curso, 'Lenguaje' AS materia, '20100005-K' AS rut, 'A_32' AS id_espacio, 1 AS bloque, 1 AS dia
    UNION ALL SELECT '1F', 'Lenguaje', '20100005-K', 'A_32', 2, 1
    UNION ALL SELECT '1F', 'Matemáticas', '20100004-1', 'A_32', 4, 1
    UNION ALL SELECT '1F', 'Electrónica', '12654321-2', 'ELECTRON', 5, 1
    UNION ALL SELECT '1F', 'Matemáticas', '20100004-1', 'A_32', 7, 1
    UNION ALL SELECT '1F', 'Ciencias Naturales', '13987654-7', 'A_32', 8, 1
    UNION ALL SELECT '1F', 'Historia', '12876543-3', 'A_32', 1, 2
    UNION ALL SELECT '1F', 'Ciencias Naturales', '13987654-7', 'A_32', 2, 2
    UNION ALL SELECT '1F', 'Inglés', '15345678-K', 'A_32', 4, 2
    UNION ALL SELECT '1F', 'Matemáticas', '20100004-1', 'A_32', 5, 2
    UNION ALL SELECT '1F', 'Electrónica', '12654321-2', 'ELECTRON', 7, 2
    UNION ALL SELECT '1F', 'Matemáticas', '20100004-1', 'A_32', 8, 2
    UNION ALL SELECT '1F', 'Lenguaje', '20100005-K', 'A_32', 1, 3
    UNION ALL SELECT '1F', 'Ciencias Naturales', '13987654-7', 'A_32', 2, 3
    UNION ALL SELECT '1F', 'Educación Física', '14765432-4', 'GIM', 4, 3
    UNION ALL SELECT '1F', 'Inglés', '15345678-K', 'A_32', 5, 3
    UNION ALL SELECT '1F', 'Matemáticas', '20100004-1', 'A_32', 7, 3
    UNION ALL SELECT '1F', 'Lenguaje', '20100005-K', 'A_32', 8, 3
    UNION ALL SELECT '1F', 'Lenguaje', '20100005-K', 'A_32', 1, 4
    UNION ALL SELECT '1F', 'Electrónica', '12654321-2', 'ELECTRON', 2, 4
    UNION ALL SELECT '1F', 'Historia', '12876543-3', 'A_32', 4, 4
    UNION ALL SELECT '1F', 'Computación', '12654321-2', 'SCC', 5, 4
    UNION ALL SELECT '1F', 'Educación Física', '14765432-4', 'GIM', 7, 4
    UNION ALL SELECT '1F', 'Matemáticas', '20100004-1', 'A_32', 8, 4
    UNION ALL SELECT '1F', 'Ciencias Naturales', '13987654-7', 'A_32', 1, 5
    UNION ALL SELECT '1F', 'Lenguaje', '20100005-K', 'A_32', 2, 5
    UNION ALL SELECT '1F', 'Orientación', '20100004-1', 'A_32', 4, 5
    UNION ALL SELECT '1F', 'Historia', '12876543-3', 'A_32', 5, 5
    UNION ALL SELECT '1F', 'Inglés', '15345678-K', 'A_32', 7, 5
    UNION ALL SELECT '1F', 'Computación', '12654321-2', 'SCC', 8, 5
    UNION ALL SELECT '1G', 'Inglés', '15345678-K', 'A_33', 1, 1
    UNION ALL SELECT '1G', 'Historia', '12876543-3', 'A_33', 2, 1
    UNION ALL SELECT '1G', 'Ciencias Naturales', '13987654-7', 'A_33', 4, 1
    UNION ALL SELECT '1G', 'Matemáticas', '20100004-1', 'A_33', 5, 1
    UNION ALL SELECT '1G', 'Lenguaje', '20100005-K', 'A_33', 7, 1
    UNION ALL SELECT '1G', 'Electrónica', '12654321-2', 'ELECTRON', 8, 1
    UNION ALL SELECT '1G', 'Lenguaje', '20100005-K', 'A_33', 1, 2
    UNION ALL SELECT '1G', 'Lenguaje', '20100005-K', 'A_33', 2, 2
    UNION ALL SELECT '1G', 'Matemáticas', '20100004-1', 'A_33', 4, 2
    UNION ALL SELECT '1G', 'Educación Física', '14765432-4', 'GIM', 5, 2
    UNION ALL SELECT '1G', 'Matemáticas', '20100004-1', 'A_33', 7, 2
    UNION ALL SELECT '1G', 'Electrónica', '12654321-2', 'ELECTRON', 8, 2
    UNION ALL SELECT '1G', 'Matemáticas', '20100004-1', 'A_33', 1, 3
    UNION ALL SELECT '1G', 'Computación', '12654321-2', 'SCC', 2, 3
    UNION ALL SELECT '1G', 'Lenguaje', '20100005-K', 'A_33', 4, 3
    UNION ALL SELECT '1G', 'Ciencias Naturales', '13987654-7', 'A_33', 5, 3
    UNION ALL SELECT '1G', 'Lenguaje', '20100005-K', 'A_33', 7, 3
    UNION ALL SELECT '1G', 'Inglés', '15345678-K', 'A_33', 8, 3
    UNION ALL SELECT '1G', 'Electrónica', '12654321-2', 'ELECTRON', 1, 4
    UNION ALL SELECT '1G', 'Historia', '12876543-3', 'A_33', 2, 4
    UNION ALL SELECT '1G', 'Ciencias Naturales', '13987654-7', 'A_33', 4, 4
    UNION ALL SELECT '1G', 'Educación Física', '14765432-4', 'GIM', 5, 4
    UNION ALL SELECT '1G', 'Computación', '12654321-2', 'SCC', 7, 4
    UNION ALL SELECT '1G', 'Ciencias Naturales', '13987654-7', 'A_33', 8, 4
    UNION ALL SELECT '1G', 'Matemáticas', '20100004-1', 'A_33', 1, 5
    UNION ALL SELECT '1G', 'Historia', '12876543-3', 'A_33', 2, 5
    UNION ALL SELECT '1G', 'Orientación', '15345678-K', 'A_33', 4, 5
    UNION ALL SELECT '1G', 'Lenguaje', '20100005-K', 'A_33', 5, 5
    UNION ALL SELECT '1G', 'Matemáticas', '20100004-1', 'A_33', 7, 5
    UNION ALL SELECT '1G', 'Inglés', '15345678-K', 'A_33', 8, 5
    UNION ALL SELECT '2A', 'Matemáticas', '20100004-1', 'A_23', 1, 1
    UNION ALL SELECT '2A', 'Matemáticas', '20100004-1', 'A_23', 2, 1
    UNION ALL SELECT '2A', 'Historia', '12876543-3', 'A_23', 4, 1
    UNION ALL SELECT '2A', 'Ciencias Naturales', '13987654-7', 'A_23', 5, 1
    UNION ALL SELECT '2A', 'Ciencias Naturales', '13987654-7', 'A_23', 7, 1
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 8, 1
    UNION ALL SELECT '2A', 'Matemáticas', '20100004-1', 'A_23', 1, 2
    UNION ALL SELECT '2A', 'Inglés', '15345678-K', 'A_23', 2, 2
    UNION ALL SELECT '2A', 'Electrónica', '12654321-2', 'ELECTRON', 4, 2
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 5, 2
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 7, 2
    UNION ALL SELECT '2A', 'Educación Física', '14765432-4', 'GIM', 8, 2
    UNION ALL SELECT '2A', 'Electrónica', '12654321-2', 'ELECTRON', 1, 3
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 2, 3
    UNION ALL SELECT '2A', 'Inglés', '15345678-K', 'A_23', 4, 3
    UNION ALL SELECT '2A', 'Matemáticas', '20100004-1', 'A_23', 5, 3
    UNION ALL SELECT '2A', 'Computación', '12654321-2', 'SCC', 7, 3
    UNION ALL SELECT '2A', 'Matemáticas', '20100004-1', 'A_23', 8, 3
    UNION ALL SELECT '2A', 'Ciencias Naturales', '13987654-7', 'A_23', 1, 4
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 2, 4
    UNION ALL SELECT '2A', 'Matemáticas', '20100004-1', 'A_23', 4, 4
    UNION ALL SELECT '2A', 'Historia', '12876543-3', 'A_23', 5, 4
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 7, 4
    UNION ALL SELECT '2A', 'Electrónica', '12654321-2', 'ELECTRON', 8, 4
    UNION ALL SELECT '2A', 'Orientación', '20100005-K', 'A_23', 1, 5
    UNION ALL SELECT '2A', 'Educación Física', '14765432-4', 'GIM', 2, 5
    UNION ALL SELECT '2A', 'Computación', '12654321-2', 'SCC', 4, 5
    UNION ALL SELECT '2A', 'Inglés', '15345678-K', 'A_23', 5, 5
    UNION ALL SELECT '2A', 'Ciencias Naturales', '13987654-7', 'A_23', 7, 5
    UNION ALL SELECT '2A', 'Historia', '12876543-3', 'A_23', 8, 5
    UNION ALL SELECT '2B', 'Electrónica', '12654321-2', 'ELECTRON', 1, 1
    UNION ALL SELECT '2B', 'Ciencias Naturales', '13987654-7', 'A_24', 2, 1
    UNION ALL SELECT '2B', 'Lenguaje', '20100005-K', 'A_24', 4, 1
    UNION ALL SELECT '2B', 'Lenguaje', '20100005-K', 'A_24', 5, 1
    UNION ALL SELECT '2B', 'Historia', '12876543-3', 'A_24', 7, 1
    UNION ALL SELECT '2B', 'Matemáticas', '20100004-1', 'A_24', 8, 1
    UNION ALL SELECT '2B', 'Inglés', '15345678-K', 'A_24', 1, 2
    UNION ALL SELECT '2B', 'Matemáticas', '20100004-1', 'A_24', 2, 2
    UNION ALL SELECT '2B', 'Lenguaje', '20100005-K', 'A_24', 4, 2
    UNION ALL SELECT '2B', 'Ciencias Naturales', '13987654-7', 'A_24', 5, 2
    UNION ALL SELECT '2B', 'Inglés', '15345678-K', 'A_24', 7, 2
    UNION ALL SELECT '2B', 'Lenguaje', '20100005-K', 'A_24', 8, 2
    UNION ALL SELECT '2B', 'Educación Física', '14765432-4', 'GIM', 1, 3
    UNION ALL SELECT '2B', 'Matemáticas', '20100004-1', 'A_24', 2, 3
    UNION ALL SELECT '2B', 'Matemáticas', '20100004-1', 'A_24', 4, 3
    UNION ALL SELECT '2B', 'Computación', '12654321-2', 'SCC', 5, 3
    UNION ALL SELECT '2B', 'Educación Física', '14765432-4', 'GIM', 7, 3
    UNION ALL SELECT '2B', 'Historia', '12876543-3', 'A_24', 8, 3
    UNION ALL SELECT '2B', 'Inglés', '15345678-K', 'A_24', 1, 4
    UNION ALL SELECT '2B', 'Ciencias Naturales', '13987654-7', 'A_24', 2, 4
    UNION ALL SELECT '2B', 'Electrónica', '12654321-2', 'ELECTRON', 4, 4
    UNION ALL SELECT '2B', 'Matemáticas', '20100004-1', 'A_24', 5, 4
    UNION ALL SELECT '2B', 'Orientación', '13987654-7', 'A_24', 7, 4
    UNION ALL SELECT '2B', 'Lenguaje', '20100005-K', 'A_24', 8, 4
    UNION ALL SELECT '2B', 'Electrónica', '12654321-2', 'ELECTRON', 1, 5
    UNION ALL SELECT '2B', 'Computación', '12654321-2', 'SCC', 2, 5
    UNION ALL SELECT '2B', 'Historia', '12876543-3', 'A_24', 4, 5
    UNION ALL SELECT '2B', 'Matemáticas', '20100004-1', 'A_24', 5, 5
    UNION ALL SELECT '2B', 'Lenguaje', '20100005-K', 'A_24', 7, 5
    UNION ALL SELECT '2B', 'Ciencias Naturales', '13987654-7', 'A_24', 8, 5
) h JOIN materias m ON m.nombre = h.materia JOIN usuarios u ON u.rut = h.rut
JOIN bloques_horarios b ON b.numero = h.bloque;

-- Anuncios (reemplaza los de ejemplo; NULL = global)
DELETE FROM anuncios;
INSERT INTO anuncios (id_curso, id_autor, titulo, contenido, prioridad)
SELECT NULL, (SELECT id_usuario FROM usuarios WHERE rut = '20100002-5'), 'Bienvenidos a LiceoMap', 'Esta es una versión de prueba con datos sintéticos.', 'INFORMATIVO'
UNION ALL SELECT NULL, (SELECT id_usuario FROM usuarios WHERE rut = '20100003-3'), 'Suspensión de clases por lluvia', 'Mañana no habrá clases en el liceo por alerta meteorológica.', 'URGENTE'
UNION ALL SELECT NULL, (SELECT id_usuario FROM usuarios WHERE rut = '13456789-9'), 'Reunión de apoderados', 'La reunión general será el próximo jueves a las 19:00 en el gimnasio.', 'RECORDATORIO'
UNION ALL SELECT '1F', (SELECT id_usuario FROM usuarios WHERE rut = '20100004-1'), 'Prueba de Matemáticas', 'El lunes se rinde la prueba del primer semestre.', 'RECORDATORIO'
UNION ALL SELECT '1G', (SELECT id_usuario FROM usuarios WHERE rut = '15345678-K'), 'Entrega de trabajo de Inglés', 'El trabajo grupal se entrega el viernes antes del recreo.', 'RECORDATORIO'
UNION ALL SELECT '2A', (SELECT id_usuario FROM usuarios WHERE rut = '20100005-K'), 'Salida pedagógica', 'Traer la autorización firmada hasta el miércoles.', 'INFORMATIVO'
UNION ALL SELECT '2B', (SELECT id_usuario FROM usuarios WHERE rut = '13987654-7'), 'Laboratorio de Ciencias', 'Traer delantal blanco para la clase del martes.', 'INFORMATIVO';
