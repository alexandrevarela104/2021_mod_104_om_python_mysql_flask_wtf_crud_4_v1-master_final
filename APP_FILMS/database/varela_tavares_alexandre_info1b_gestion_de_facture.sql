-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: varela_tavares_alexandre_info1b_gestion_de_facture

-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS varela_tavares_alexandre_info1b_gestion_de_facture;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS varela_tavares_alexandre_info1b_gestion_de_facture;

-- Utilisation de cette base de donnée

USE varela_tavares_alexandre_info1b_gestion_de_facture;
-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_destinataire`
--

CREATE TABLE `t_avoir_destinataire` (
  `id_avoir_destinataire` int(11) NOT NULL,
  `fk_facture` int(11) NOT NULL,
  `fk_destinataire` int(11) NOT NULL,
  `enregistrement` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avoir_destinataire`
--

INSERT INTO `t_avoir_destinataire` (`id_avoir_destinataire`, `fk_facture`, `fk_destinataire`, `enregistrement`) VALUES
(1, 1, 1, '2021-06-08 03:46:46'),
(2, 2, 2, '2021-06-08 03:46:46'),
(3, 3, 3, '2021-06-08 03:46:46'),
(4, 4, 4, '2021-06-08 03:46:46'),
(5, 11, 3, '2021-06-08 03:46:46'),
(6, 12, 4, '2021-06-08 03:46:46'),
(7, 13, 3, '2021-06-08 03:46:46');

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_motif`
--

CREATE TABLE `t_avoir_motif` (
  `id_avoir_motif` int(11) NOT NULL,
  `fk_facture` int(11) NOT NULL,
  `fk_motif` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avoir_motif`
--

INSERT INTO `t_avoir_motif` (`id_avoir_motif`, `fk_facture`, `fk_motif`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 1),
(5, 12, 3);

-- --------------------------------------------------------

--
-- Structure de la table `t_destinataire`
--

CREATE TABLE `t_destinataire` (
  `id_destinataire` int(11) NOT NULL,
  `destinataire` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_destinataire`
--

INSERT INTO `t_destinataire` (`id_destinataire`, `destinataire`) VALUES
(1, 'Groupe Mutuel'),
(2, 'BCV'),
(3, 'Gérance ville'),
(4, 'Vaudoise'),
(5, 'Groupes assurances suisses contonales');

-- --------------------------------------------------------

--
-- Structure de la table `t_email`
--

CREATE TABLE `t_email` (
  `id_email` int(11) NOT NULL,
  `email` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_email`
--

INSERT INTO `t_email` (`id_email`, `email`) VALUES
(1, 'alexbenifca@gmail.com'),
(2, 'bigkichta@gmail.com'),
(3, 'marlene@hotmail.ch'),
(4, 'orgorgorg@gmail.com'),
(5, 'mamanangai@lkdfaéjs.ch');

-- --------------------------------------------------------

--
-- Structure de la table `t_facture`
--

CREATE TABLE `t_facture` (
  `id_facture` int(11) NOT NULL,
  `reception` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `numero_facture` int(11) NOT NULL,
  `somme` float NOT NULL,
  `delai` date NOT NULL,
  `payement` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_facture`
--

INSERT INTO `t_facture` (`id_facture`, `reception`, `numero_facture`, `somme`, `delai`, `payement`) VALUES
(1, '2021-06-08 07:28:09', 2021, 500, '2021-04-01', '2021-06-10'),
(2, '2021-03-16 19:00:00', 2000, 423.25, '2021-03-31', '2021-06-01'),
(3, '2021-06-08 07:28:38', 312, 500, '2021-03-31', '2021-06-17'),
(4, '2020-12-10 19:00:00', 21, 50, '2021-07-14', '2021-06-08'),
(10, '2021-06-08 07:28:29', 12, 313, '2021-06-02', '2021-06-01'),
(11, '2012-10-19 14:00:00', 23, 34, '2012-10-20', '2012-10-20'),
(12, '2012-10-19 14:00:00', 423, 423, '2012-10-20', '2012-10-20'),
(13, '2021-06-08 07:28:53', 853, 900, '2021-06-16', '2021-06-11'),
(14, '2021-06-08 06:16:58', 312, 231, '2012-10-10', '2012-10-10'),
(15, '2021-06-08 07:29:29', 321, 500, '2021-09-10', '2021-08-20');

-- --------------------------------------------------------

--
-- Structure de la table `t_motif`
--

CREATE TABLE `t_motif` (
  `id_motif` int(11) NOT NULL,
  `motif` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_motif`
--

INSERT INTO `t_motif` (`id_motif`, `motif`) VALUES
(1, 'Assurance Maladie'),
(2, 'Amende pour retard de payement'),
(3, 'Souris ');

-- --------------------------------------------------------

--
-- Structure de la table `t_user`
--

CREATE TABLE `t_user` (
  `id_user` int(11) NOT NULL,
  `nom_user` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_user`
--

INSERT INTO `t_user` (`id_user`, `nom_user`, `password`) VALUES
(2, 'marie2', 'rooter'),
(3, 'gaspar12', 'gaspargaspar'),
(4, 'marlene', 'password'),
(5, 'bigkischta', 'jfaiefe');

-- --------------------------------------------------------

--
-- Structure de la table `t_user_email`
--

CREATE TABLE `t_user_email` (
  `id_user_email` int(11) NOT NULL,
  `fk_user` int(11) DEFAULT NULL,
  `fk_email` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_user_email`
--

INSERT INTO `t_user_email` (`id_user_email`, `fk_user`, `fk_email`) VALUES
(2, 3, 4),
(3, 3, 5);

-- --------------------------------------------------------

--
-- Structure de la table `t_user_facture`
--

CREATE TABLE `t_user_facture` (
  `id_user_facture` int(11) NOT NULL,
  `fk_user` int(11) NOT NULL,
  `fk_facture` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_user_facture`
--

INSERT INTO `t_user_facture` (`id_user_facture`, `fk_user`, `fk_facture`) VALUES
(1, 2, 1),
(2, 3, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 12);

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_avoir_destinataire`
--
ALTER TABLE `t_avoir_destinataire`
  ADD PRIMARY KEY (`id_avoir_destinataire`),
  ADD KEY `fk_facture` (`fk_facture`),
  ADD KEY `fk_destinataire` (`fk_destinataire`);

--
-- Index pour la table `t_avoir_motif`
--
ALTER TABLE `t_avoir_motif`
  ADD PRIMARY KEY (`id_avoir_motif`),
  ADD KEY `fk_facture` (`fk_facture`),
  ADD KEY `fk_motif` (`fk_motif`);

--
-- Index pour la table `t_destinataire`
--
ALTER TABLE `t_destinataire`
  ADD PRIMARY KEY (`id_destinataire`);

--
-- Index pour la table `t_email`
--
ALTER TABLE `t_email`
  ADD PRIMARY KEY (`id_email`);

--
-- Index pour la table `t_facture`
--
ALTER TABLE `t_facture`
  ADD PRIMARY KEY (`id_facture`);

--
-- Index pour la table `t_motif`
--
ALTER TABLE `t_motif`
  ADD PRIMARY KEY (`id_motif`);

--
-- Index pour la table `t_user`
--
ALTER TABLE `t_user`
  ADD PRIMARY KEY (`id_user`);

--
-- Index pour la table `t_user_email`
--
ALTER TABLE `t_user_email`
  ADD PRIMARY KEY (`id_user_email`),
  ADD KEY `fk_user` (`fk_user`),
  ADD KEY `fk_email` (`fk_email`);

--
-- Index pour la table `t_user_facture`
--
ALTER TABLE `t_user_facture`
  ADD PRIMARY KEY (`id_user_facture`),
  ADD KEY `fk_facture` (`fk_facture`),
  ADD KEY `fk_user` (`fk_user`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_avoir_destinataire`
--
ALTER TABLE `t_avoir_destinataire`
  MODIFY `id_avoir_destinataire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT pour la table `t_avoir_motif`
--
ALTER TABLE `t_avoir_motif`
  MODIFY `id_avoir_motif` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_destinataire`
--
ALTER TABLE `t_destinataire`
  MODIFY `id_destinataire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_email`
--
ALTER TABLE `t_email`
  MODIFY `id_email` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_facture`
--
ALTER TABLE `t_facture`
  MODIFY `id_facture` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT pour la table `t_motif`
--
ALTER TABLE `t_motif`
  MODIFY `id_motif` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_user`
--
ALTER TABLE `t_user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_user_email`
--
ALTER TABLE `t_user_email`
  MODIFY `id_user_email` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_user_facture`
--
ALTER TABLE `t_user_facture`
  MODIFY `id_user_facture` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_avoir_destinataire`
--
ALTER TABLE `t_avoir_destinataire`
  ADD CONSTRAINT `t_avoir_destinataire_ibfk_1` FOREIGN KEY (`fk_facture`) REFERENCES `t_facture` (`id_facture`),
  ADD CONSTRAINT `t_avoir_destinataire_ibfk_2` FOREIGN KEY (`fk_destinataire`) REFERENCES `t_destinataire` (`id_destinataire`);

--
-- Contraintes pour la table `t_avoir_motif`
--
ALTER TABLE `t_avoir_motif`
  ADD CONSTRAINT `t_avoir_motif_ibfk_1` FOREIGN KEY (`fk_facture`) REFERENCES `t_facture` (`id_facture`),
  ADD CONSTRAINT `t_avoir_motif_ibfk_2` FOREIGN KEY (`fk_motif`) REFERENCES `t_motif` (`id_motif`);

--
-- Contraintes pour la table `t_user_email`
--
ALTER TABLE `t_user_email`
  ADD CONSTRAINT `t_user_email_ibfk_1` FOREIGN KEY (`fk_user`) REFERENCES `t_user` (`id_user`),
  ADD CONSTRAINT `t_user_email_ibfk_2` FOREIGN KEY (`fk_email`) REFERENCES `t_email` (`id_email`);

--
-- Contraintes pour la table `t_user_facture`
--
ALTER TABLE `t_user_facture`
  ADD CONSTRAINT `t_user_facture_ibfk_1` FOREIGN KEY (`fk_user`) REFERENCES `t_user` (`id_user`),
  ADD CONSTRAINT `t_user_facture_ibfk_2` FOREIGN KEY (`fk_facture`) REFERENCES `t_facture` (`id_facture`);